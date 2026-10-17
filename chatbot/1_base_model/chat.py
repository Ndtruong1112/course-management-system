import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("🤖 CHATBOT: BASE MODEL (MÔ HÌNH NỀN - CHƯA ĐƯỢC HUẤN LUYỆN VỚI CODEBASE)")
print("Model ID: Qwen/Qwen2.5-Coder-1.5B-Instruct (Gốc)")
print("=" * 70)

base_model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
has_cuda = torch.cuda.is_available()

print(f"Thiết bị: {'CUDA (GPU: ' + torch.cuda.get_device_name(0) + ')' if has_cuda else 'CPU'}")
print("Đang nạp Base Model gốc (4-bit)...")

if has_cuda:
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
else:
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

tokenizer = AutoTokenizer.from_pretrained(base_model_id)
model.eval()

print("\n[SẴN SÀNG] Bạn có thể hỏi bất kỳ câu hỏi nào. Gõ 'exit' hoặc 'quit' để thoát.\n")

while True:
    try:
        user_input = input("Bạn (hỏi Base): ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break

        messages = [
            {"role": "system", "content": "Bạn là trợ lý AI hữu ích."},
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
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        print(f"\n[Base Model]:\n{response}\n")
        print("-" * 70)

    except (KeyboardInterrupt, EOFError):
        print("\nĐã thoát chương trình.")
        break
