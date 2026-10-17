import os
import sys
import argparse
import json
import torch

# Chuyển bộ nhớ đệm HuggingFace sang ổ D (tránh làm đầy ổ C đang chỉ còn 3.3 GB)
os.environ["HF_HOME"] = r"D:\.cache\huggingface"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser(description="Huấn luyện mô hình QLoRA tối ưu VRAM cho dự án")
parser.add_argument("--model", "-m", choices=["7b", "3b", "1.5b"], default="7b",
                    help="Chọn mô hình nền: 7b (Qwen2.5-Coder-7B), 3b (Qwen2.5-Coder-3B), hoặc 1.5b (mặc định: 7b)")
parser.add_argument("--steps", "-s", type=int, default=100, help="Số bước train (mặc định: 100)")
args = parser.parse_args()

MODEL_MAP = {
    "7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "3b": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "1.5b": "Qwen/Qwen2.5-Coder-1.5B-Instruct"
}

model_id = MODEL_MAP[args.model]
dataset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.jsonl")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

print("=" * 70)
print(f"KHỞI ĐỘNG CHƯƠNG TRÌNH FINE-TUNING VỚI MÔ HÌNH: {model_id}")
print("Áp dụng kỹ thuật phân mảnh tính toán & tiết kiệm VRAM tối đa")
print("=" * 70)

# 1. Kiểm tra GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Thiết bị: {device}")
if device == "cuda":
    free_vram = torch.cuda.mem_get_info()[0] / (1024**3)
    total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM khả dụng: {free_vram:.2f} GB / {total_vram:.2f} GB")
else:
    print("CẢNH BÁO: Không tìm thấy GPU CUDA! Train trên CPU sẽ rất chậm.")

print(f"\nThư mục tải cache: D:\\.cache\\huggingface (an toàn cho ổ C)")

# 2. Cấu hình lượng tử hóa 4-bit (QLoRA)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

print(f"\nĐang tải Tokenizer và Model '{model_id}'...")
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)

# 3. Cấu hình LoRA Adapter và Kỹ thuật "Cắt nhỏ" theo dung lượng model
if args.model == "7b":
    # Cấu hình siêu tiết kiệm VRAM cho 7B trên GPU 6GB
    batch_size = 1
    grad_accum = 16          # Cắt nhỏ: 16 bước tích lũy gradient trước khi cập nhật 1 lần
    max_seq_len = 512        # Giới hạn độ dài ngữ cảnh để không tràn VRAM
    use_gradient_checkpointing = True
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"], # Chỉ train 2 module cốt lõi để giữ VRAM an toàn
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
elif args.model == "3b":
    batch_size = 1
    grad_accum = 8
    max_seq_len = 768
    use_gradient_checkpointing = True
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
else: # 1.5b
    batch_size = 2
    grad_accum = 4
    max_seq_len = 1024
    use_gradient_checkpointing = False
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

model = get_peft_model(model, peft_config)
print("\nThông tin các tham số có thể huấn luyện (Trainable Parameters):")
model.print_trainable_parameters()

# 4. Nạp và xử lý tập dữ liệu Chat
print("\nĐang chuẩn bị dữ liệu...")
raw_dataset = load_dataset("json", data_files=dataset_file, split="train")

def format_chat(batch):
    formatted_texts = []
    for messages in batch["messages"]:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        formatted_texts.append(text)
    return {"text": formatted_texts}

formatted_dataset = raw_dataset.map(format_chat, batched=True)

# 5. Cấu hình siêu tham số huấn luyện
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=batch_size,
    gradient_accumulation_steps=grad_accum,
    learning_rate=2e-4,
    logging_steps=5,
    max_steps=args.steps,
    save_strategy="no",
    fp16=True,
    optim="paged_adamw_8bit",                 # Chống tràn VRAM: tự động tràn sang RAM hệ thống khi cần
    gradient_checkpointing=use_gradient_checkpointing, # Giảm 60% VRAM activation
    warmup_ratio=0.05,
    lr_scheduler_type="cosine",
    report_to="none"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=formatted_dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_len,
    tokenizer=tokenizer,
    args=training_args
)

# 6. BẮT ĐẦU HUẤN LUYỆN
print("\n" + "=" * 70)
print(f"BẮT ĐẦU HUẤN LUYỆN ({args.steps} steps, Micro-batch: {batch_size}, Accumulation: {grad_accum})...")
print("=" * 70)

torch.cuda.empty_cache()
trainer.train()

# 7. Lưu kết quả LoRA Adapter
final_lora_dir = os.path.join(output_dir, "course-management-lora-adapter")
print(f"\nĐang lưu trọng số LoRA vào: {final_lora_dir}")
trainer.model.save_pretrained(final_lora_dir)
tokenizer.save_pretrained(final_lora_dir)

# Ghi lại metadata base_model_id vào file cấu hình
config_path = os.path.join(final_lora_dir, "model_meta.json")
with open(config_path, "w", encoding="utf-8") as f:
    json.dump({"base_model_id": model_id, "model_tier": args.model}, f, indent=2)

print("\n" + "=" * 70)
print(f"HUẤN LUYỆN THÀNH CÔNG CHO MÔ HÌNH {model_id}!")
print(f"Adapter đã được lưu tại: {final_lora_dir}")
print("=" * 70)
