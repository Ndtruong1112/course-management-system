import os
import sys
import json
import torch

os.environ["HF_HOME"] = r"D:\.cache\huggingface"

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lora_dir = os.path.join(base_dir, "outputs", "course-management-lora-adapter")

if not os.path.exists(lora_dir):
    print(f"\n[LỖI]: Chưa tìm thấy thư mục LoRA Adapter tại '{lora_dir}'.")
    print("Vui lòng chạy 'python train_local.py' ở thư mục gốc trước!")
    sys.exit(1)

# Tự động phát hiện Base Model đã dùng trong adapter
base_model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
adapter_config_path = os.path.join(lora_dir, "adapter_config.json")
if os.path.exists(adapter_config_path):
    try:
        with open(adapter_config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            base_model_id = cfg.get("base_model_name_or_path", base_model_id)
    except Exception:
        pass

print("=" * 70)
print("🚀 CHATBOT: FINE-TUNED MODEL (ĐÃ HUẤN LUYỆN VỚI CODEBASE)")
print(f"Base Model: {base_model_id} + QLoRA Adapter")
print("=" * 70)

has_cuda = torch.cuda.is_available()
print(f"Thiết bị: {'CUDA (GPU: ' + torch.cuda.get_device_name(0) + ')' if has_cuda else 'CPU'}")
print("Đang nạp Base Model và LoRA Adapter...")

if has_cuda:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
else:
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

tokenizer = AutoTokenizer.from_pretrained(lora_dir)
model = PeftModel.from_pretrained(base_model, lora_dir)
model.eval()

print("\n[SẴN SÀNG] Chuyên gia AI của dự án Course Management System đã sẵn sàng!")
print("Bạn có thể hỏi bất kỳ câu hỏi nào về codebase. Gõ 'exit' hoặc 'quit' để thoát.\n")

while True:
    try:
        user_input = input("Bạn (hỏi Fine-tuned): ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break

        messages = [
            {"role": "system", "content": "Bạn là trợ lý AI chuyên gia, nắm vững 100% kiến trúc, mã nguồn và nghiệp vụ của dự án Course Management System (Hệ thống Quản lý Khóa học, Học viên & Tài liệu MinIO)."},
            {"role": "user", "content": user_input}
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        if has_cuda:
            inputs = inputs.to("cuda")

        print("Đang suy nghĩ...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=2048,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        print(f"\n[AI Fine-tuned]:\n{response}\n")
        print("-" * 70)

    except (KeyboardInterrupt, EOFError):
        print("\nĐã thoát chương trình.")
        break
