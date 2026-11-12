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
1. **Chế độ "⚡ So sánh Song song (A/B)"**: Bạn chỉ cần gõ 1 câu hỏi, giao diện sẽ chia làm 2 cột hiển thị đồng thời câu trả lời của **Base Model** và **Fine-tuned Model** để thấy rõ sự khác biệt.
2. **Chế độ "🚀 Chỉ Fine-tuned"**: Chỉ chat với mô hình đã học codebase.
3. **Chế độ "🌐 Chỉ Base Model"**: Chỉ chat với mô hình gốc ngoài Internet.
4. **Nút gợi ý câu hỏi nhanh (Quick Prompts)**: Click 1 chạm để hỏi ngay các câu hỏi kinh điển về `SearchCriteria`, sinh code DAO mới, hoặc giải thích MinIO versioning.

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
