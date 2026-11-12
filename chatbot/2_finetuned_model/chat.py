import os
import sys
import json
import time
import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

os.environ["HF_HOME"] = r"D:\.cache\huggingface"

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lora_dir = os.path.join(base_dir, "outputs", "course-management-lora-adapter")
env_path = os.path.join(base_dir, ".env")

# Nạp Gemini API Key
gemini_api_key = ""
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                gemini_api_key = line.split("=", 1)[1].strip()

if not os.path.exists(lora_dir):
    print(f"\n[LỖI]: Chưa tìm thấy thư mục LoRA Adapter tại '{lora_dir}'.")
    print("Vui lòng chạy 'python train_local.py' ở thư mục gốc trước!")
    sys.exit(1)

# Tự động phát hiện Base Model
base_model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
sharded_model_path = r"D:\models\Qwen2.5-Coder-3B-Instruct-sharded"
model_load_path = sharded_model_path if os.path.exists(sharded_model_path) else base_model_id

adapter_config_path = os.path.join(lora_dir, "adapter_config.json")
if os.path.exists(adapter_config_path):
    try:
        with open(adapter_config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            base_model_id = cfg.get("base_model_name_or_path", base_model_id)
    except Exception:
        pass

print("=" * 70)
print("🤖 CHATBOT: TRỢ LÝ AI NỘI BỘ (HYBRID LOCAL-FIRST)")
print(f"Local Brain: {base_model_id} (GPU RTX 4050)")
print(f"Cloud Assistant: {'Google Gemini Sẵn sàng' if gemini_api_key else 'Chưa cấu hình'}")
print("=" * 70)

has_cuda = torch.cuda.is_available()
print(f"Thiết bị: {'CUDA (GPU: ' + torch.cuda.get_device_name(0) + ')' if has_cuda else 'CPU'}")
print("Đang nạp Base Model và LoRA Adapter...")

local_ready = False
base_model = None
model = None
tokenizer = None

try:
    if has_cuda:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            model_load_path,
            quantization_config=bnb_config,
            device_map="auto"
        )
    else:
        base_model = AutoModelForCausalLM.from_pretrained(
            model_load_path,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    tokenizer = AutoTokenizer.from_pretrained(lora_dir)
    model = PeftModel.from_pretrained(base_model, lora_dir)
    model.eval()
    local_ready = True
    print("-> Đã nạp Base Model và LoRA Adapter thành công!\n")
except Exception as e:
    print(f"[CẢNH BÁO]: Chưa thể nạp mô hình Local trực tiếp ({e}).")
    print("-> Hệ thống chuyển sang chế độ Cloud AI Assistant với đầy đủ kiến trúc Codebase dự án.\n")

def is_heavy_task(msg):
    if not local_ready:
        return True
    msg_l = msg.lower()
    heavy_kws = [
        "tạo cho tôi 1 project", "tạo project mới", "project mới", "dự án mới", 
        "hệ thống mới", "viết toàn bộ", "toàn bộ hệ thống", "full project", 
        "viết cả project", "tạo một hệ thống", "xây dựng hệ thống", "quản lý thuê phòng cho 1 khách sạn"
    ]
    return any(kw in msg_l for kw in heavy_kws)

def call_cloud_gemini(user_msg):
    system_instruction = (
        "Bạn là Kiến trúc sư Phần mềm Cao cấp chuyên gia Spring Boot 3 và Java 21. "
        "Bạn được giao nhiệm vụ viết mã nguồn dựa trên các chuẩn mực kiến trúc cốt lõi của dự án Course Management System:\n"
        "1. Entity JPA: Dùng Jakarta Persistence (@Entity, @Table, @Id, @GeneratedValue, @Index, Lombok @Getter, @Setter, @Builder...).\n"
        "2. Tầng DAO: Phải kế thừa HibernatePaginationSortingDao<Pk, Entity> và dùng EntityManager tạo các câu lệnh HQL/JPQL động, an toàn kiểu dữ liệu.\n"
        "3. Tầng Service & Controller: Tách rõ Interface/Impl, dùng DTO Pattern và xử lý ngoại lệ tập trung qua @RestControllerAdvice.\n"
        "4. TÍNH CHẤT BẮT BUỘC: Khi người dùng yêu cầu tạo dự án mới (ví dụ Khách sạn, Bán hàng, Thư viện, Bệnh viện...) "
        "BẠN PHẢI VIẾT MÃ NGUỒN JAVA ĐẦY ĐỦ CHO TỪNG FILE (Entity, DAO, Service, Controller). Tuyệt đối không dùng văn mẫu lý thuyết suông!"
    )
    prompt = f"{system_instruction}\n\n[YÊU CẦU CỦA NGƯỜI DÙNG]:\n{user_msg}"
    models = ['gemini-2.5-flash', 'gemini-3.5-flash', 'gemini-3-flash-preview']
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_api_key}"
        try:
            res = requests.post(url, json={'contents': [{'parts': [{'text': prompt}]}]}, timeout=45)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            continue
    return "Lỗi: Không thể kết nối tới Cloud AI."

print("\n[SẴN SÀNG] Hệ thống Local AI làm chủ đã sẵn sàng!")
print("- Tác vụ vừa/nhỏ (giải thích, viết 1 DAO): Local tự sinh offline.")
print("- Tác vụ lớn (tạo cả project mới): Local tự động ủy quyền Cloud Gemini viết full code.")
print("Gõ 'exit' hoặc 'quit' để thoát.\n")

while True:
    try:
        user_input = input("Bạn hỏi: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break

        if is_heavy_task(user_input) and gemini_api_key:
            print("\n[LOCAL AI ROUTER]: Phát hiện yêu cầu tạo dự án lớn...")
            print("-> Local AI đang đóng gói kiến trúc dự án và ủy quyền cho Cloud AI (Gemini) sinh full code...")
            cloud_res = call_cloud_gemini(user_input)
            print(f"\n🌐 [CLOUD AI ĐƯỢC ỦY QUYỀN]:\n{cloud_res}\n")
        else:
            print("\n[LOCAL AI ROUTER]: Tác vụ phù hợp, Local AI tự xử lý trực tiếp trên GPU...")
            messages = [
                {"role": "system", "content": "Bạn là kỹ sư AI phần mềm cao cấp, chuyên gia kiến trúc Spring Boot 3, Java 21, Hibernate Generic DAO và JPA. Khi người dùng yêu cầu tạo dự án mới hoặc viết code, bạn LUÔN LUÔN VIẾT MÃ NGUỒN JAVA ĐẦY ĐỦ."},
                {"role": "user", "content": user_input}
            ]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(prompt, return_tensors="pt")
            if has_cuda:
                inputs = inputs.to("cuda")

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=2048,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1
                )

            response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            print(f"\n⚡ [LOCAL AI TỰ SINH TRỰC TIẾP]:\n{response}\n")

        print("-" * 70)

    except (KeyboardInterrupt, EOFError):
        print("\nĐã thoát chương trình.")
        break
