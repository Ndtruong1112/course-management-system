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
├── web_app.py               # ỨNG DỤNG WEB STUDIO (SSE Streaming, nhiều chế độ, chấm điểm heuristic)
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

### Chọn model, RAG và độ dài câu trả lời

Mặc định, chatbot chỉ nạp thư viện AI, tokenizer và trọng số khi lần đầu chọn
xử lý local hoặc yêu cầu AI local chấm điểm. Mở giao diện, báo cáo hoặc dùng
Cloud/Zero Context không tự nạp model local. Lần gọi local đầu tiên cần thêm
thời gian tải; các lượt sau dùng lại model.

Nếu không có CUDA, chatbot không tự nạp model 3B FP32 vào RAM vì có thể cần
rất nhiều bộ nhớ. Có thể chủ động đặt `LOCAL_ALLOW_CPU=true` nếu máy đủ RAM;
đặt `LOCAL_MODEL_AUTOSTART=true` nếu muốn nạp sẵn model khi khởi động. Model
không tự được dỡ khỏi bộ nhớ sau khi nạp; dừng chatbot để giải phóng.


Chế độ local và cột fine-tuned luôn gọi LoRA đã nạp, kể cả khi câu hỏi không
liên quan dự án hoặc không rõ ý. Cột base chạy model gốc với LoRA tắt. Nếu
adapter chưa nạp, ứng dụng báo lỗi thay vì âm thầm dùng base. LoRA vẫn có thể
trả lời thiên về dự án do dữ liệu fine-tune; kết quả được hiển thị nguyên bản để
có thể so sánh, không thay bằng câu trả lời dựng sẵn.

Ở thanh bên, **RAG cho Fine-tuned local** có ba lựa chọn: tự động (dựa trên quy
tắc nhận diện câu hỏi), luôn bật ngữ cảnh dự án, hoặc tắt. Chọn **tắt** khi muốn
so sánh base và LoRA không kèm tài liệu dự án; câu hỏi không cần đúng cú pháp.
Cột zero-context chỉ nhận câu hỏi hiện tại và không có system prompt hoặc lịch
sử; vì vậy so sánh nó với local là so sánh cấu hình hệ thống, không phải đo riêng
hiệu quả fine-tune. RAG có thể đưa mã dự án vào prompt nếu bật.

**Giới hạn token local** cho phép chọn độ dài tối đa. Nếu model chạm giới hạn,
giao diện báo câu trả lời có thể bị cắt; ở chế độ chat đơn có nút **Tiếp tục**.
Nếu kết nối gián đoạn, giao diện thông báo lỗi thay vì coi phản hồi đã hoàn tất.
Giới hạn này không áp dụng cho nhà cung cấp cloud, vốn có cấu hình riêng.
Cloud hiển thị cảnh báo khi nhà cung cấp báo hết token hoặc luồng bị ngắt;
không tự ghép phản hồi của model khác sau khi đã nhận một phần. Giao diện không
lưu hoặc hiển thị lịch sử phiên; ngữ cảnh gần đây chỉ giữ trong phiên đang mở.
Dữ liệu lịch sử phiên đã lưu từ trước vẫn nằm trong bộ nhớ trình duyệt, không tự xóa.

### Đánh giá trực tiếp câu trả lời

Sau khi phản hồi hoàn tất, mỗi câu trả lời có mục **Đánh giá câu trả lời**.
Chọn **AI đề xuất điểm** để base model local xem câu hỏi và câu trả lời theo bốn
tiêu chí: đúng yêu cầu (30), đầy đủ (25), tính hợp lý nhìn thấy trong câu trả lời
(25) và trình bày (20). AI đề xuất mức 0–4 và nhận xét cho từng tiêu chí; ứng
dụng quy đổi theo trọng số, làm tròn từng tiêu chí và cộng điểm tổng 0–100.
Bảng chi tiết là đề xuất gốc của AI, còn điểm và nhận xét
bạn xác nhận có thể được chỉnh sửa. Model chấm chỉ là hỗ trợ: không tự đối chiếu codebase,
không chạy mã hay xác nhận sự thật, và không độc lập với base đang được so sánh.
Bạn có thể chọn **Tự chấm**, sửa điểm/nhận xét và bấm **Xác nhận đánh giá**.
Nhận xét đã xác nhận lưu trong localStorage của trình duyệt; xóa dữ liệu trình
duyệt sẽ xóa các nhận xét đó. Đánh giá trực tiếp không tự ghi vào kết quả
benchmark, vì benchmark có bộ câu hỏi và quy trình chấm riêng.

### OpenRouter Zero Context

Chọn **OpenRouter Zero Context** trong thanh bên, chọn Particle-1, North Mini
Code, Flint, Nemotron 3.5 Lightning hoặc Free Router, rồi gửi câu hỏi. Cần có
`OPENROUTER_API_KEY` trong `.env` hoặc biến môi trường. Các lựa chọn là phiên bản
miễn phí tại thời điểm cấu hình, nhưng nhà cung cấp có thể giới hạn quota, thay
đổi hoặc ngừng model. Model cụ thể không tự động chuyển sang model khác nếu lỗi;
Free Router có thể chọn model khác nhau giữa các lần gọi.

Trong chế độ này, máy chủ chỉ gửi câu hỏi hiện tại, không tự thêm system prompt,
RAG hay lịch sử chat. Bất kỳ thông tin nào bạn tự đưa vào câu hỏi vẫn được gửi
cho OpenRouter và nhà cung cấp. Bộ chọn cũng áp dụng cho cột zero-context trong
chế độ So Sánh Hệ Thống và Đấu Trường 3 Chiều. Điểm kiến trúc là heuristic dựa
trên từ khóa, không xác nhận mã biên dịch hay tính đúng đắn.

Chatbot mặc định chỉ lắng nghe trên `127.0.0.1`; Docker Compose ánh xạ cổng về
localhost. Các chế độ cloud khác có thể gửi ngữ cảnh dự án, tùy chế độ được chọn.

### Các tính năng trên giao diện Web:
1. **Thanh Gợi Ý Sinh Mã Nguồn (Quick Prompts - Ghim cố định ở thanh trên cùng)**:
   - Ghim sẵn 8 bài toán sinh mã nguồn kiến trúc kinh điển: `Module Giảng Viên`, `Dynamic HQL DAO`, `DTO & Validation`, `Lưu trữ MinIO`, `Đăng Ký Khóa Học`, `Lọc Đa Tiêu Chí`, `Bảo Mật & Phân Quyền`, `Scaffold Dự Án Mới`. Click 1 chạm là tự động điền và kích hoạt.
2. **Bộ Đôi Nút Điều Khiển Tích Hợp Ngay Trong Khung Chat (In-Chat Dual Action Buttons)**:
   - **Nút "⚡ Chức năng"**: Bấm vào nút (hoặc gõ phím `/`) để mở menu popup gồm **9 tính năng chuyên biệt** (tách biệt hoàn toàn, không trùng lặp):
     - ⚡ **Chế Độ Xử Lý AI (3 chế độ)**: Hybrid Auto, 100% Local GPU RTX 4050, Cloud Gemini.
     - 🛠️ **Công Cụ Hệ Thống (6 tiện ích)**: Mở báo cáo nghiệm thu trực quan (`/benchmark-report`), Swagger API Docs (`:8080`), Web quản lý CMS (`:8080`), Quét lại RAG Codebase, Tạo phiên mới, Làm mới màn hình.
     - Hỗ trợ tìm kiếm tức thì, phím tắt **ESC** để đóng, **Enter** để chọn nhanh.
   - **Nút "⚖️ Đối Chiếu & Đánh Giá" (Nằm ngay cạnh nút Chức năng)**: Bấm vào để trồi lên menu chọn nhanh 4 chế độ so sánh:
     - ⚖️ **So Sánh Mô Hình**: Base vs Fine-tuned QLoRA GPU (chạy 100% offline RTX 4050).
     - 📋 **So Sánh Hệ Thống**: Hệ thống dự án (LoRA + RAG) vs AI Tiêu chuẩn bên ngoài (Zero-Context).
     - 📊 **Đấu Trường 3 Chiều**: Chạy lần lượt 3 luồng AI để đối chiếu.
     - 🤖 **So Sánh Với Claude**: Đối chiếu trực tiếp với Claude và đánh giá từng câu trả lời.
     - Nút tự động đổi tên và hiển thị huy hiệu theo chế độ so sánh đang kích hoạt (`So Sánh Model`, `So Sánh Hệ Thống`, `Đấu Trường 3 Chiều`, `So Sánh Claude`).
3. **Chế độ so sánh A/B và đấu trường 3 chiều**: Gõ một câu hỏi; các model chạy lần lượt và giao diện chia cột để đối chiếu câu trả lời với scorecard 5 tiêu chí heuristic.

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
