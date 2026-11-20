# Course Management System — hướng dẫn cho Antigravity

Trả lời bằng tiếng Việt. Dùng code đang có làm nguồn xác nhận; README và skill
có thể cũ hơn code. Mục tiêu là hoàn thành yêu cầu, giữ chức năng, giảm chi phí
ngữ cảnh và tránh làm tăng áp lực RAM trên máy khoảng 16 GB / RTX 4050.

## Chọn ngữ cảnh

- Việc xuyên tầng, chưa rõ phạm vi: `.agents/skills/cms-task-flow/SKILL.md`.
- Java / DAO / Service / REST / MinIO: `.agents/skills/cms-backend/SKILL.md`.
- Giao diện web quản lý hoặc Studio: `.agents/skills/cms-frontend/SKILL.md`.
- Qwen / LoRA / RAG / streaming / Cloud routing: `.agents/skills/cms-local-ai/SKILL.md`.
- AI chấm output, rubric, benchmark: `.agents/skills/cms-output-evaluation/SKILL.md`.
- Crash, RAM cao, không mở được localhost: `.agents/skills/cms-runtime-debug/SKILL.md`.

Chỉ đọc skill và đoạn code liên quan. Một câu hỏi giải thích ngắn không cần
khởi động hệ thống, đọc toàn repo hoặc tạo kế hoạch nhiều trang.

## Cách làm việc

1. Đọc yêu cầu hiện tại và `git status --short`; giữ các thay đổi đang có.
2. Dùng `rg` tìm symbol, đọc caller và implementation trước khi sửa.
3. Nêu ngắn phần sẽ sửa. Tiếp tục công việc đã được người dùng cho phép;
   không hỏi lại cùng một quyền. Tôn trọng các giới hạn thực thi của nền tảng.
4. Không tự deploy, push, reset Git, xóa dữ liệu, đổi khóa AES, đóng app hoặc
   chạy benchmark GPU chỉ vì đang kiểm tra code. Những việc này cần phạm vi
   cho phép cụ thể. Không đưa secret hoặc toàn bộ `.env` vào báo cáo.
5. Kiểm chứng tương xứng với thay đổi. Không tự viết test cho thay đổi nhỏ chỉ
   để kiểm tra câu chữ. Đối với quy trình test có giới hạn riêng của dự án,
   áp dụng yêu cầu kiểm thử đã được người dùng cho phép trong nhiệm vụ đó.
6. Báo thay đổi, bằng chứng đã chạy và phần chưa kiểm tra. Không suy ra chạy
   đúng ngoài thực tế chỉ từ unit test hoặc HTTP 200.

Giữ quy chuẩn kỹ thuật hiện có trong `cms-standards` và `springboot-standards`;
không sao chép hoặc nạp toàn bộ hai skill đó cho mỗi việc. Khi quy định xung
đột với chỉ dẫn rõ ràng của người dùng, tuân theo chỉ dẫn có hiệu lực trong phiên.
