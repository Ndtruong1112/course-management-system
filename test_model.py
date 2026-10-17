import os
import sys
import random
import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# NGÂN HÀNG CÂU HỎI KIỂM THỬ ĐA DẠNG (QUESTION BANK)
# ==============================================================================
QUESTION_BANK = [
    # ── Chủ đề 1: Kiến trúc Generic DAO & Hibernate ──
    {
        "category": "Generic DAO & Hibernate",
        "question": "Trong dự án Course Management System, lớp DAO cha tổng quát hỗ trợ phân trang và sắp xếp có tên là gì và kế thừa từ những lớp nào?"
    },
    {
        "category": "Generic DAO & Hibernate",
        "question": "Giải thích các phương thức tìm kiếm đặc thù được viết trong CourseDaoImpl ngoài các hàm CRUD cơ bản."
    },
    {
        "category": "Generic DAO & Hibernate",
        "question": "Tại sao dự án lại kết hợp cả SimpleJpaRepository của Spring Data JPA với Hibernate Generic DAO tự viết?"
    },

    # ── Chủ đề 2: Lưu trữ MinIO, Soft Delete & Versioning ──
    {
        "category": "MinIO Storage & Versioning",
        "question": "Trong CSDL của Course Management System, bảng documents liên kết với hồ sơ nghiệp vụ qua trường khóa ngoại nào?"
    },
    {
        "category": "MinIO Storage & Versioning",
        "question": "Giải thích cơ chế nâng version của tài liệu khi người dùng upload file trùng tên trong DocumentServiceImpl."
    },
    {
        "category": "MinIO Storage & Versioning",
        "question": "Cơ chế Xóa mềm (Soft Delete) đối với tài liệu trong DocumentServiceImpl được thực hiện như thế nào và mang lại lợi ích gì?"
    },
    {
        "category": "MinIO Storage & Versioning",
        "question": "File nhị phân vật lý (PDF, Word, Ảnh) được lưu ở đâu, còn cơ sở dữ liệu quan hệ MySQL lưu trữ những thông tin gì?"
    },

    # ── Chủ đề 3: JPA Dynamic Specification & Criteria API ──
    {
        "category": "JPA Specification",
        "question": "Dự án Course Management System triển khai tìm kiếm động đa điều kiện bằng GenericSpecification và Criteria API như thế nào?"
    },
    {
        "category": "JPA Specification",
        "question": "Lớp SearchCriteria trong package specification giữ vai trò gì và hỗ trợ những toán tử so sánh nào?"
    },

    # ── Chủ đề 4: Cấu trúc Dự án & Xử lý lỗi ──
    {
        "category": "Kiến trúc & Exception Handling",
        "question": "Dự án Course Management System gồm những package chính nào và vai trò của từng package là gì?"
    },
    {
        "category": "Kiến trúc & Exception Handling",
        "question": "Cơ chế xử lý lỗi tập trung (Global Exception Handling) trong dự án được tổ chức bằng những class nào?"
    },

    # ── Chủ đề 5: Sinh mã nguồn mới (Code Generation) ──
    {
        "category": "Code Generation Task",
        "question": "Hãy viết một phương thức tìm kiếm học viên theo số điện thoại trong StudentDaoImpl bằng câu lệnh HQL theo chuẩn của dự án."
    },
    {
        "category": "Code Generation Task",
        "question": "Hãy viết cấu trúc lớp CategoryDaoImpl kế thừa HibernatePaginationSortingDao để quản lý Entity Category theo đúng chuẩn kiến trúc của dự án."
    }
]

def main():
    parser = argparse.ArgumentParser(description="Kiểm thử mô hình AI Fine-tuned (Course Management System)")
    parser.add_argument("--num", "-n", type=int, default=3, help="Số lượng câu hỏi ngẫu nhiên muốn kiểm tra (mặc định: 3)")
    parser.add_argument("--all", "-a", action="store_true", help="Chạy toàn bộ ngân hàng câu hỏi")
    parser.add_argument("--interactive", "-i", action="store_true", help="Chế độ chat tương tác trực tiếp với mô hình")
    args = parser.parse_args()

    base_model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    lora_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs", "course-management-lora-adapter")

    print("=" * 70)
    print("KIỂM THỬ MÔ HÌNH SAU KHI FINE-TUNING (COURSE MANAGEMENT SYSTEM)")
    print("=" * 70)

    if not os.path.exists(lora_dir):
        print(f"\n[LỖI]: Chưa tìm thấy thư mục LoRA Adapter tại:")
        print(f"       -> '{lora_dir}'")
        print("\n[HƯỚNG DẪN]: Hãy chạy lệnh huấn luyện trước:")
        print("             python train_local.py")
        sys.exit(1)

    has_cuda = torch.cuda.is_available()
    print(f"Thiết bị khả dụng: {'CUDA (GPU: ' + torch.cuda.get_device_name(0) + ')' if has_cuda else 'CPU'}")

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
        print("[LƯU Ý]: Chạy trên CPU không hỗ trợ 4-bit BitsAndBytes, đang nạp ở chế độ float32...")
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    tokenizer = AutoTokenizer.from_pretrained(lora_dir)
    model = PeftModel.from_pretrained(base_model, lora_dir)
    model.eval()

    print("[OK] Mô hình và Adapter đã sẵn sàng phục vụ!\n")

    def ask(question, category=None):
        header = f"[{category}] " if category else ""
        print(f"\n❓ {header}Câu hỏi: {question}")
        print("-" * 70)

        messages = [
            {"role": "system", "content": "Bạn là trợ lý AI chuyên gia, nắm vững 100% kiến trúc, mã nguồn và nghiệp vụ của dự án Course Management System."},
            {"role": "user", "content": question}
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt")
        if has_cuda:
            inputs = inputs.to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        print(f"🤖 AI Trả lời:\n{response.strip()}\n")
        print("=" * 70)

    # 1. Chế độ chat tương tác trực tiếp
    if args.interactive:
        print(">>> CHẾ ĐỘ TƯƠNG TÁC TRỰC TIẾP (Gõ 'exit' hoặc 'quit' để thoát) <<<")
        while True:
            try:
                user_q = input("\nBạn hỏi: ").strip()
                if not user_q:
                    continue
                if user_q.lower() in ['exit', 'quit']:
                    print("Tạm biệt!")
                    break
                ask(user_q)
            except (KeyboardInterrupt, EOFError):
                print("\nĐã thoát chương trình.")
                break
        return

    # 2. Chế độ chạy toàn bộ bộ câu hỏi
    if args.all:
        print(f">>> ĐANG CHẠY TOÀN BỘ {len(QUESTION_BANK)} CÂU HỎI TRONG NGÂN HÀNG <<<")
        for idx, item in enumerate(QUESTION_BANK, 1):
            print(f"\n[Test Case {idx}/{len(QUESTION_BANK)}]")
            ask(item["question"], item["category"])
        return

    # 3. Chế độ ngẫu nhiên (Mặc định)
    num_to_pick = min(args.num, len(QUESTION_BANK))
    selected_questions = random.sample(QUESTION_BANK, num_to_pick)

    print(f">>> ĐANG BỐC NGẪU NHIÊN {num_to_pick} CÂU HỎI TỪ NGÂN HÀNG ({len(QUESTION_BANK)} CÂU) <<<")
    for idx, item in enumerate(selected_questions, 1):
        print(f"\n[Ngẫu nhiên {idx}/{num_to_pick}]")
        ask(item["question"], item["category"])

    print("\n[MẸO]:")
    print(" - Để bốc 5 câu ngẫu nhiên:   python test_model.py -n 5")
    print(" - Để chat trực tiếp với AI:  python test_model.py -i")
    print(" - Để chạy tất cả câu hỏi:   python test_model.py --all")

if __name__ == "__main__":
    main()
