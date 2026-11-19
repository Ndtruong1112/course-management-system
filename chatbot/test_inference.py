import os
import sys
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

os.environ["HF_HOME"] = r"D:\.cache\huggingface"
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lora_dir = os.path.join(root_dir, "outputs", "course-management-lora-adapter")
sharded_model_path = r"D:\models\Qwen2.5-Coder-3B-Instruct-sharded"

tokenizer = AutoTokenizer.from_pretrained(lora_dir)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

base_model = AutoModelForCausalLM.from_pretrained(
    sharded_model_path,
    quantization_config=bnb_config,
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, lora_dir)
model.eval()

prompt = "Tạo Module Quản lý Giảng viên (Instructor Entity + DAO kế thừa Generic DAO)"
messages = [
    {"role": "system", "content": "Bạn là chuyên gia Spring Boot 3 và Java 21 cho dự án Course Management System. Hãy viết mã nguồn đầy đủ, chính xác theo kiến trúc dự án."},
    {"role": "user", "content": prompt}
]
formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(formatted, return_tensors="pt").to("cuda")

print("Generated formatted prompt:")
print(repr(formatted))

if torch.cuda.is_available():
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
started = time.perf_counter()
with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

if torch.cuda.is_available():
    torch.cuda.synchronize()
elapsed = time.perf_counter() - started

gen_tokens = outputs[0][inputs.input_ids.shape[1]:]
print(f"Generation: {len(gen_tokens)} tokens / {elapsed:.2f}s ({len(gen_tokens) / elapsed:.1f} tokens/s)")
if torch.cuda.is_available():
    print(f"GPU allocated: {torch.cuda.memory_allocated() / 1024**2:.0f} MiB; peak: {torch.cuda.max_memory_allocated() / 1024**2:.0f} MiB")
print("Generated token IDs:", gen_tokens.tolist())
resp = tokenizer.decode(gen_tokens, skip_special_tokens=False)
print("Decoded with special tokens:")
print(repr(resp))
