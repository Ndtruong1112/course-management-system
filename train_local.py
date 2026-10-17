import os
import sys
import torch
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

print("=" * 60)
print("KHỞI ĐỘNG CHƯƠNG TRÌNH FINE-TUNING CHO DỰ ÁN COURSE-MANAGEMENT-SYSTEM")
print("=" * 60)

# 1. Kiểm tra phần cứng GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Thiết bị tính toán: {device}")
if device == "cuda":
    print(f"Tên GPU: {torch.cuda.get_device_name(0)}")
    print(f"Tổng VRAM khả dụng: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
else:
    print("CẢNH BÁO: Không tìm thấy GPU CUDA! Quá trình train trên CPU sẽ rất chậm.")

# 2. Chọn Model nền (Base Model)
model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
dataset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.jsonl")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

print(f"\nBase Model: {model_id}")
print(f"File Dataset: {dataset_file}")

# 3. Cấu hình lượng tử hóa 4-bit (QLoRA) để tiết kiệm VRAM tối đa
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

print("\nĐang tải Tokenizer và Model...")
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

# 4. Cấu hình LoRA Adapter
peft_config = LoraConfig(
    r=16,                         # Rank của ma trận LoRA
    lora_alpha=32,                # Hệ số tỉ lệ LoRA
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)
print("\nThông tin các tham số có thể huấn luyện (Trainable Parameters):")
model.print_trainable_parameters()

# 5. Nạp và xử lý tập dữ liệu Chat
print("\nĐang chuẩn bị dữ liệu...")
raw_dataset = load_dataset("json", data_files=dataset_file, split="train")

def format_chat(batch):
    formatted_texts = []
    for messages in batch["messages"]:
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        formatted_texts.append(text)
    return {"text": formatted_texts}

formatted_dataset = raw_dataset.map(format_chat, batched=True)

# 6. Cấu hình siêu tham số huấn luyện (Training Arguments)
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=5,
    max_steps=120,                  # Huấn luyện 120 bước để mô hình ghi nhớ vững chắc kiến trúc
    save_strategy="no",
    fp16=True,
    optim="paged_adamw_8bit",      # Trình tối ưu 8-bit chống tràn VRAM
    warmup_ratio=0.05,
    lr_scheduler_type="cosine",
    report_to="none"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=formatted_dataset,
    dataset_text_field="text",
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=training_args
)

# 7. BẮT ĐẦU HUẤN LUYỆN
print("\n" + "=" * 60)
print("BẮT ĐẦU QUÁ TRÌNH HUẤN LUYỆN (TRAINING)...")
print("=" * 60)

trainer.train()

# 8. Lưu kết quả LoRA Adapter
final_lora_dir = os.path.join(output_dir, "course-management-lora-adapter")
print(f"\nĐang lưu trọng số LoRA vào: {final_lora_dir}")
trainer.model.save_pretrained(final_lora_dir)
tokenizer.save_pretrained(final_lora_dir)

print("\n" + "=" * 60)
print("HUẤN LUYỆN THÀNH CÔNG! ĐÃ CẬP NHẬT TRỌNG SỐ CHO MÔ HÌNH!")
print(f"Adapter đã được lưu tại: {final_lora_dir}")
print("=" * 60)
