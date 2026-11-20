---
name: cms-local-ai
description: Maintains Qwen LoRA loading, project RAG, local generation, SSE streaming, and provider routing in Course Studio. Use when local models fail, answers drift toward the project, or local and cloud behavior needs correction.
---

# AI local, RAG và provider

Đọc các hàm đang được gọi trong `chatbot/web_app.py`; intent ở
`message_intent.py`, retrieval ở `rag_engine.py`, zero-context ở
`openrouter_zero.py`. Không đổi cloud model của ứng dụng chỉ vì người dùng
chọn một model khác cho coding agent Antigravity.

## Invariants cần giữ

- Model Qwen và các thư viện ML nặng được nạp khi cần. Import Flask, mở UI,
  đổi mode hoặc health check không được tự nạp Torch/weights.
- Giữ kiểm tra bộ nhớ Windows trước nạp; chưa đủ RAM thì báo rõ và cho thử
  lại sau khi tài nguyên thay đổi. Không mặc định fallback CPU cho model 3B.
- Tokenizer, base và adapter local dùng tệp/cache với `local_files_only=True`.
  Thiếu tệp phải báo, không tự download weights hàng GB.
- Base và LoRA dùng chung weights, bật/tắt adapter dưới generation lock.
  Không nạp thêm model base để tạo cột so sánh. Không báo fine-tuned khi thiếu adapter.
- Giữ LoRA được gọi với câu hỏi chung khi người dùng đang so sánh; intent chỉ
  quyết định prompt/RAG. Không giả lập câu trả lời chào hỏi để làm đẹp benchmark.
- Zero-context chỉ gửi câu hỏi hiện tại, đúng model được chọn, không kèm lịch
  sử, system prompt dự án hoặc RAG. Không thay model im lặng khi lỗi/quota.
- Mode local không gọi Cloud. Hybrid có thể delegate nhiệm vụ lớn theo
  `is_heavy_task`; xác nhận routing thực tế trước khi quy lỗi Internet.

## Streaming và lỗi

Giữ schema SSE mà `processStreamEvent` xử lý, bao gồm start/chunk/done/error.
Thread sinh phải kết thúc streamer khi gặp exception. Phân biệt stop, length,
interrupted và error; chạm token không đồng nghĩa thành công đầy đủ.
Không ghép phần đầu từ model A với phần cuối model B hoặc retry sau partial
output như thể cùng một câu trả lời.

Trình duyệt kết nối HTTP localhost ngay cả khi inference offline. Khi có
`Failed to fetch`, kiểm tra server/cổng/log trước khi đổi API key hoặc provider.
Không in secret vào UI/log; giữ thông báo đủ thông tin để chẩn đoán tải model.

## Chọn phép thử

Kiểm tra prompt/routing bằng mock trước. Chỉ chạy GPU thật khi có yêu cầu hoặc
cần xác minh lỗi model và còn đủ tài nguyên. Một câu ngắn, token thấp đủ kiểm
tra đường chạy; không suy ra chất lượng sinh mã từ phép thử đó. Benchmark CLI
nạp bản model riêng: không chạy cùng chatbot đã nạp model trên máy này.
