---
name: cms-frontend
description: Improves the CMS admin frontend and Course Studio interface while preserving API contracts, streaming, model controls, and browser memory limits. Use for HTML, CSS, JavaScript, responsive layout, or frontend performance work here.
---

# Frontend CMS và Course Studio

## Xác định đúng giao diện

- Web quản lý: `src/main/resources/static/index.html`, cổng 8080.
- Studio: `HTML_TEMPLATE` trong `chatbot/web_app.py`, CSS ở
  `chatbot/static/studio.css`, cổng 7860.
- Nghiệm thu: `chatbot/templates/benchmark_report.html`.

Không tạo app React, thêm framework hoặc thay trang khác khi chỉ sửa giao diện
hiện có. Đọc handler và caller trước khi thay DOM.

## Giữ chức năng

Studio phải giữ chọn mode, model zero-context, RAG, token limit, gửi câu hỏi,
streaming, tiếp tục phản hồi, toolbar code, so sánh và đánh giá có xác nhận.
Giữ ID/data attributes mà JavaScript sử dụng, hoặc sửa tất cả caller cùng lúc.
Không tái thêm lịch sử phiên: người dùng đã yêu cầu bỏ; ngữ cảnh ngắn của
cuộc trò chuyện đang mở vẫn có ích. Không xóa localStorage đánh giá/API key.

Hiển thị output bằng `textContent` hoặc Markdown đã sanitize; không tin HTML
từ model, exception, provider hay dữ liệu lưu trong browser. Không bỏ DOMPurify
để tránh lỗi render. Nếu thư viện không có, dùng văn bản an toàn.

Với admin: duy trì search/filter/page trên server, bỏ qua response cũ khi
người dùng tìm kiếm mới. Giữ entity được chọn khi chỉnh sửa dù entity nằm ngoài
trang đầu. Download có xác thực và giới hạn memory cho nhánh fallback Blob.

## Hiệu năng và trải nghiệm

- Đọc profiler/DOM/caller trước khi kết luận CSS là nguyên nhân ăn hàng GB RAM.
- Tránh render lại toàn trang hoặc serialize toàn hội thoại theo mỗi chunk.
  Nếu throttle render, flush chunk cuối, error và finish; đo trước/sau.
- Không thêm animation/timer/listener không có lifecycle cleanup. Không tự
  xóa câu trả lời đang hiển thị để giảm RAM mà không có thiết kế rõ ràng.
- Giữ focus, label, keyboard, trạng thái loading/error và bố cục mobile.
- Local inference và offline frontend khác nhau: Studio vẫn có thư viện CDN.
  Muốn offline toàn bộ phải đưa đúng phiên bản thư viện về local và kiểm tra lại.

## Kiểm chứng

Chọn test JS theo giao diện. Render template để bắt lỗi Jinja và URL static.
Khi có browser, xem desktop/mobile và thao tác các chức năng bị chạm tới.
Nếu browser không khả dụng, nói rõ chưa visual QA; không tự cài/chạy nhiều
trình duyệt chỉ để lấy screenshot trên máy thiếu RAM.
