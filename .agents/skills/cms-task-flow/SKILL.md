---
name: cms-task-flow
description: Coordinates cross-layer changes and scoped codebase reviews in Course Management System. Use when a task spans Java backend, Flask Studio, or model evaluation and the relevant files are not yet clear.
---

# Điều phối công việc CMS

## Định tuyến

- API nghiệp vụ: `src/main/java/com/mkii/coursemanagementsystem/`.
- Web quản lý cổng 8080: `src/main/resources/static/index.html`.
- Studio cổng 7860: `chatbot/web_app.py`, `chatbot/static/studio.css`.
- Báo cáo nghiệm thu: `chatbot/templates/benchmark_report.html`.
- Model/RAG: `chatbot/message_intent.py`, `rag_engine.py`, `openrouter_zero.py`.
- Benchmark: `benchmark/evaluate.py`, `evaluation_core.py`, `cases.jsonl`.
- Khởi động: `start_all.bat` gọi `scripts/start_local.bat`; script con
  `run_backend.bat` và `run_chatbot.bat`. Không xem tab trình duyệt là bằng chứng server còn sống.

## Thực hiện

1. Xác định kết quả người dùng cần và ví dụ kích hoạt cụ thể. Nếu chỉ một thông
   tin chưa rõ làm thay đổi cách triển khai đáng kể, hỏi một câu và tiếp tục
   các bước độc lập; không mở quy trình phê duyệt cho lựa chọn triển khai thường lệ.
2. Xác định luồng dữ liệu từ UI → route → service/helper → nơi lưu hoặc provider.
   Mở file liên quan theo symbol, không đọc `outputs/`, model weights, dataset
   hoặc toàn bộ log. Phân biệt mã của app với câu lệnh/nội dung do model sinh ra.
3. Đọc skill chuyên môn cần thiết theo đường dẫn trong `GEMINI.md`. Nếu có
   quy chuẩn cũ sai so với code, ghi nhận chênh lệch thay vì sửa code cho khớp mô tả cũ.
4. Sửa tối thiểu nhưng đủ các caller; không chỉ tạo helper chưa được dùng.
   Giữ nguyên thay đổi người dùng; không tự commit để "backup" toàn workspace.
5. Khi cần kiểm chứng, chọn lệnh trong [verification.md](references/verification.md).
   Dừng khi bằng chứng đủ; chỉ chạy rộng hơn khi có thay đổi/rủi ro mới.

## Hoàn thành

Nêu hành vi trước/sau, file chính, lệnh và kết quả kiểm chứng, giới hạn còn lại.
Nếu chỉ kiểm tra một phần, gọi đúng phạm vi đó. Với vấn đề lặp lại, so sánh
bằng chứng mới với lần trước thay vì tiếp tục thêm quy tắc hoặc dependency.
