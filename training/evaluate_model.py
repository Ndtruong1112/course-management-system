import os
import sys
import json
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) == "training" else script_dir
chatbot_dir = os.path.join(root_dir, "chatbot")
if chatbot_dir not in sys.path:
    sys.path.insert(0, chatbot_dir)

from rag_engine import CodebaseRAG

lora_dir = os.path.join(root_dir, "outputs", "course-management-lora-adapter")
base_model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"

# Tự động phát hiện base model từ adapter config
adapter_config = os.path.join(lora_dir, "adapter_config.json")
if os.path.exists(adapter_config):
    try:
        with open(adapter_config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            base_model_id = cfg.get("base_model_name_or_path", base_model_id)
    except Exception:
        pass

print("=" * 70)
print("HỆ THỐNG ĐÁNH GIÁ ĐỘ CHÍNH XÁC (EVALUATION BENCHMARK)")
print("DỰ ÁN: COURSE MANAGEMENT SYSTEM")
print(f"MÔ HÌNH: {base_model_id} (Fine-tuned LoRA + Codebase RAG)")
print("=" * 70)

rag_engine = CodebaseRAG(root_dir)

sharded_model_path = r"D:\models\Qwen2.5-Coder-3B-Instruct-sharded"
model_load_path = sharded_model_path if os.path.exists(sharded_model_path) else base_model_id

if not os.path.exists(lora_dir):
    print(f"LỖI: Không tìm thấy adapter tại {lora_dir}")
    print("Vui lòng chạy 'train_local.py' trước để huấn luyện mô hình!")
    sys.exit(1)

# Nạp model
print("Đang nạp mô hình để kiểm thử...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(lora_dir)
base_model = AutoModelForCausalLM.from_pretrained(
    model_load_path,
    quantization_config=bnb_config,
    device_map="auto"
)
model = PeftModel.from_pretrained(base_model, lora_dir)
model.eval()

# TẬP DỮ LIỆU TEST ĐỘC LẬP (TEST SET)
test_suite = [
    {
        "id": 1,
        "category": "Cơ sở dữ liệu & Khóa ngoại Document",
        "question": "Trong CSDL của Course Management System, bảng documents liên kết với hồ sơ nghiệp vụ qua trường khóa ngoại nào?",
        "keywords": ["app_detail_fk", "appid"],
        "min_matches": 1
    },
    {
        "id": 2,
        "category": "Nghiệp vụ Versioning",
        "question": "Khi upload tài liệu trùng tên trong cùng một hồ sơ, trường nào của bản ghi cũ sẽ bị chuyển về false?",
        "keywords": ["active", "active = false"],
        "min_matches": 1
    },
    {
        "id": 3,
        "category": "Nghiệp vụ Versioning",
        "question": "Khi tài liệu bị trùng tên, phiên bản (version) của file mới được tính như thế nào?",
        "keywords": ["+ 1", "tăng", "version + 1"],
        "min_matches": 1
    },
    {
        "id": 4,
        "category": "Xóa mềm (Soft Delete)",
        "question": "Chức năng xóa tài liệu trong DocumentServiceImpl làm gì để không bị mất dữ liệu vĩnh viễn?",
        "keywords": ["deleted", "deleted = true", "xóa mềm"],
        "min_matches": 1
    },
    {
        "id": 5,
        "category": "Kiến trúc Lưu trữ MinIO",
        "question": "File nhị phân vật lý (PDF, DOCX) được lưu ở đâu, còn cơ sở dữ liệu quan hệ lưu cái gì?",
        "keywords": ["minio", "metadata"],
        "min_matches": 2
    },
    {
        "id": 6,
        "category": "Kiến trúc Generic DAO",
        "question": "Lớp DAO cha tổng quát hỗ trợ phân trang và sắp xếp trong dự án có tên là gì?",
        "keywords": ["hibernatepaginationsortingdao", "hibernategenericdao"],
        "min_matches": 1
    },
    {
        "id": 7,
        "category": "Thực thể Course",
        "question": "Thực thể Course trong Course Management System gồm những thuộc tính chính nào?",
        "keywords": ["title", "price", "duration", "description"],
        "min_matches": 2
    },
    {
        "id": 8,
        "category": "Truy vấn DAO Mở rộng",
        "question": "Lớp CourseDaoImpl cung cấp những phương thức truy vấn mở rộng cụ thể nào ngoài CRUD cơ bản?",
        "keywords": ["searchbytitle", "findbypricerange"],
        "min_matches": 1
    },
    {
        "id": 9,
        "category": "Thực thể Student & Ràng buộc",
        "question": "Trong thực thể Student, trường thông tin nào có ràng buộc duy nhất (unique = true)?",
        "keywords": ["email"],
        "min_matches": 1
    },
    {
        "id": 10,
        "category": "REST Controller API",
        "question": "Ba tiền tố URL gốc (base endpoints) được định nghĩa trong ApiConstants là những đường dẫn nào?",
        "keywords": ["/api/courses", "/api/students", "/api/documents"],
        "min_matches": 2
    }
]

print(f"\nBắt đầu chạy bộ kiểm thử gồm {len(test_suite)} câu hỏi đánh giá độc lập...\n")

def run_single_eval(question, use_rag=False):
    system_prompt = (
        "Bạn là chuyên gia kỹ thuật của dự án Course Management System (com.mkii.coursemanagementsystem). "
        "Hãy trả lời chính xác tên class, tên trường, annotation và endpoint dựa đúng theo mã nguồn thật."
    )
    rag_files = []
    final_user = question
    if use_rag:
        rag_block, rag_files = rag_engine.format_context_block(question, top_k=3, max_chars=2800)
        if rag_block:
            final_user = f"{rag_block}\n\n[CÂU HỎI]:\n{question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_user}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    start_time = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=False,
            repetition_penalty=1.12,
            pad_token_id=tokenizer.eos_token_id
        )
    elapsed = time.time() - start_time
    answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
    return answer, round(elapsed, 2), rag_files


results = []
lora_correct_count = 0
rag_correct_count = 0

for item in test_suite:
    q = item["question"]
    print(f"[{item['id']}/{len(test_suite)}] Chủ đề: {item['category']}")
    print(f"Câu hỏi: {q}")

    ans_lora, t_lora, _ = run_single_eval(q, use_rag=False)
    matched_lora = [kw for kw in item["keywords"] if kw.lower() in ans_lora.lower()]
    passed_lora = len(matched_lora) >= item["min_matches"]
    if passed_lora:
        lora_correct_count += 1

    ans_rag, t_rag, rag_files = run_single_eval(q, use_rag=True)
    matched_rag = [kw for kw in item["keywords"] if kw.lower() in ans_rag.lower()]
    passed_rag = len(matched_rag) >= item["min_matches"]
    if passed_rag:
        rag_correct_count += 1

    print(f"  [LoRA Only]     {'PASSED' if passed_lora else 'FAILED'} ({len(matched_lora)}/{item['min_matches']}: {matched_lora}) - {t_lora}s")
    print(f"  [LoRA + RAG]    {'PASSED' if passed_rag else 'FAILED'} ({len(matched_rag)}/{item['min_matches']}: {matched_rag}) - {t_rag}s | RAG: {rag_files}")
    print(f"  Trả lời (LoRA + RAG): {ans_rag}")
    print("-" * 70)

    results.append({
        "id": item["id"],
        "category": item["category"],
        "question": q,
        "lora_only": {"answer": ans_lora, "passed": passed_lora, "matched": matched_lora, "time": t_lora},
        "lora_rag": {"answer": ans_rag, "passed": passed_rag, "matched": matched_rag, "time": t_rag, "rag_files": rag_files},
        "answer": ans_rag,
        "passed": passed_rag,
        "matched": matched_rag
    })

# TÍNH TOÁN BÁO CÁO TỔNG KẾT
lora_acc = (lora_correct_count / len(test_suite)) * 100
rag_acc = (rag_correct_count / len(test_suite)) * 100

print("\n" + "=" * 70)
print("BÁO CÁO TỔNG KẾT ĐỘ CHÍNH XÁC (FINAL BENCHMARK REPORT)")
print("=" * 70)
print(f"Tổng số câu hỏi kiểm thử : {len(test_suite)}")
print(f"Độ chính xác LoRA thuần  : {lora_correct_count}/{len(test_suite)} ({lora_acc:.2f}%)")
print(f"Độ chính xác LoRA + RAG  : {rag_correct_count}/{len(test_suite)} ({rag_acc:.2f}%)")
print("=" * 70)

# Xuất kết quả ra file eval_report.json
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({
        "total": len(test_suite),
        "passed": rag_correct_count,
        "accuracy_percent": rag_acc,
        "lora_only_passed": lora_correct_count,
        "lora_only_accuracy_percent": lora_acc,
        "rag_lora_passed": rag_correct_count,
        "rag_lora_accuracy_percent": rag_acc,
        "details": results
    }, f, ensure_ascii=False, indent=2)

print(f"Chi tiết đánh giá đã được lưu vào: {report_path}")
