# Hệ thống AI Chatbot Phân luồng & Đối sánh (Course Management System)

Thư mục này được tổ chức tách biệt làm 2 luồng mô hình và đi kèm giao diện Web UI trực quan để bạn dễ dàng hỏi đáp, trình diễn và đối sánh trước thầy giáo:

```text
chatbot/
├── 1_base_model/            # LUỒNG 1: Mô hình gốc (Chưa gắn LoRA Adapter)
│   ├── chat.py              # Script chat CLI độc lập với Base Model
│   └── README.md            # Giải thích vai trò của Base Model
│
├── 2_finetuned_model/       # LUỒNG 2: Mô hình đã Fine-tune bằng QLoRA (Am hiểu Codebase)
│   ├── chat.py              # Script chat CLI độc lập với Fine-tuned Model
│   └── README.md            # Giải thích vai trò của Fine-tuned Model
│
├── rag_engine.py            # CodebaseRAG & Bộ đánh giá tuân thủ kiến trúc 5 tiêu chí
├── web_app.py               # ỨNG DỤNG WEB STUDIO (SSE Streaming, 7 chế độ, chấm điểm đồng bộ)
├── Dockerfile               # Đóng gói container dịch vụ AI Chatbot
├── requirements.txt         # Thư viện Python AI
└── README.md                # Tài liệu hướng dẫn sử dụng
```

---

## 🚀 Cách 1: Sử dụng Giao diện Web Chatbot (Khuyên dùng)

Nhấp đúp vào **`scripts/run_chatbot.bat`** (hoặc chạy lệnh từ gốc dự án):
```bash
python chatbot/web_app.py
```
Sau đó mở trình duyệt web và truy cập địa chỉ:
👉 **`http://localhost:7860`**

### Các tính năng trên giao diện Web:
1. **Thanh Gợi Ý Sinh Mã Nguồn (Quick Prompts - Ghim cố định ở thanh trên cùng)**:
   - Ghim sẵn 8 bài toán sinh mã nguồn kiến trúc kinh điển: `Module Giảng Viên`, `Dynamic HQL DAO`, `DTO & Validation`, `Lưu trữ MinIO`, `Đăng Ký Khóa Học`, `Lọc Đa Tiêu Chí`, `Bảo Mật & Phân Quyền`, `Scaffold Dự Án Mới`. Click 1 chạm là tự động điền và kích hoạt.
2. **Bộ Đôi Nút Điều Khiển Tích Hợp Ngay Trong Khung Chat (In-Chat Dual Action Buttons)**:
   - **Nút "⚡ Chức năng"**: Bấm vào nút (hoặc gõ phím `/`) để mở menu popup gồm **9 tính năng chuyên biệt** (tách biệt hoàn toàn, không trùng lặp):
     - ⚡ **Chế Độ Xử Lý AI (3 chế độ)**: Hybrid Auto, 100% Local GPU RTX 4050, Cloud Gemini 1M Context.
     - 🛠️ **Công Cụ Hệ Thống (6 tiện ích)**: Mở báo cáo nghiệm thu trực quan (`/benchmark-report`), Swagger API Docs (`:8080`), Web quản lý CMS (`:8080`), Quét lại RAG Codebase, Tạo phiên mới, Làm mới màn hình.
     - Hỗ trợ tìm kiếm tức thì, phím tắt **ESC** để đóng, **Enter** để chọn nhanh.
   - **Nút "⚖️ Đối Chiếu & Đánh Giá" (Nằm ngay cạnh nút Chức năng)**: Bấm vào để trồi lên menu chọn nhanh 4 chế độ so sánh:
     - ⚖️ **So Sánh Mô Hình**: Base vs Fine-tuned QLoRA GPU (chạy 100% offline RTX 4050).
     - 📋 **So Sánh Hệ Thống**: Hệ thống dự án (LoRA + RAG) vs AI Tiêu chuẩn bên ngoài (Zero-Context).
     - 📊 **Đấu Trường 3 Chiều**: Chạy song song 3 luồng AI cùng lúc.
     - 🤖 **So Sánh Với Claude**: Đối chiếu trực tiếp với Claude và tự động chấm điểm tuân thủ kiến trúc 5 tiêu chí.
     - Nút tự động đổi tên và hiển thị huy hiệu theo chế độ so sánh đang kích hoạt (`So Sánh Model`, `So Sánh Hệ Thống`, `Đấu Trường 3 Chiều`, `So Sánh Claude`).
3. **Chế độ "⚡ So sánh Song song (A/B) & Đấu trường 3 chiều"**: Gõ 1 câu hỏi, giao diện chia cột hiển thị đồng thời câu trả lời của Base Model, Fine-tuned Model và Cloud AI/Claude để đối chiếu kiến trúc tự động với scorecard 5 tiêu chí.

---

## 💻 Cách 2: Sử dụng dòng lệnh Terminal độc lập (CLI)

- **Nếu bạn chỉ muốn hỏi mô hình gốc (Base Model)**:
  ```bash
  cd chatbot/1_base_model
  python chat.py
  ```

- **Nếu bạn chỉ muốn hỏi mô hình chuyên gia dự án (Fine-tuned Model)**:
  ```bash
  cd chatbot/2_finetuned_model
  python chat.py
  ```
