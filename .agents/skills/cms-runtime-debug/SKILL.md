---
name: cms-runtime-debug
description: Diagnoses excessive RAM, crashes, startup failures, and localhost connection errors in CMS on Windows. Use for runtime incidents and resource investigations, rather than ordinary feature edits.
---

# Chẩn đoán runtime Windows

## Thu bằng chứng trước

Chạy `Get-Help .agents/skills/cms-runtime-debug/scripts/inspect-runtime.ps1 -Detailed`
rồi chạy script nếu cần snapshot RAM, nhóm process và kết nối cổng. Script chỉ
đọc, không nạp model, không in command line chứa token, không dừng process.
Snapshot hiện tại không chứng minh trạng thái lúc ảnh chụp hoặc nguyên nhân crash.

| Dấu hiệu | Kiểm tra tiếp theo |
|---|---|
| Failed to fetch / network error | TCP tới localhost:7860, HTTP GET nhẹ, PID và log gần thời điểm lỗi |
| Trang mở nhưng không gửi được | Trang có thể còn trong browser sau khi server dừng |
| Model load ValueError | Chi tiết exception đã che secret, RAM/commit, VRAM, model path và CUDA |
| RAM cao | Working set và private commit của từng process; phân biệt app, Maven, backend, editor LSP |
| Cloud quota/network | Provider đã chọn, HTTP status, thời điểm partial output; không đổi model im lặng |

Nếu TCP state trong `netstat` không khớp, thử kết nối bằng TcpClient. HTTP 200
ở `/` chỉ chứng minh web server; không chứng minh model đã nạp hay DB sẵn sàng.

## Chẩn đoán và sửa

1. Tái hiện nhẹ nhất có thể. Lỗi không tái hiện được thì thu log thay vì đoán.
   Không in `.env` hoặc command line toàn hệ thống để tìm secret.
2. Xác định process thuộc project bằng PID, executable, caller và cổng; cổng
   bị dùng không phải quyền được kill process. Không tự đóng Edge, IDE, AnyDesk,
   Defender, database hoặc service Windows.
3. `run_backend.bat` build rồi chạy JAR để Maven thoát. Không quay lại dùng
   `spring-boot:run` thường trực như một cách "tối ưu". Heap cap không bao gồm
   native memory, GPU, process con hay tổng working set.
4. Khi được phép restart dịch vụ, báo phạm vi, xác minh PID lại ngay trước
   khi dừng và giữ lại log; không áp dụng PID cũ trong tài liệu hoặc hội thoại.
   Helper nền trên Windows dùng `Start-Process -WindowStyle Hidden`.
5. So sánh idle và sau tác vụ với cùng điều kiện. Số nhóm process có trang
   nhớ dùng chung, không cộng máy móc thành tổng RAM vật lý.

Nếu mở model để thử, thu cả RAM/private commit/VRAM và trả tài nguyên của
tiến trình thử khi xong. Không tự thay đổi paging file, GPU driver, RAM hệ
thống hoặc JVM toàn cục. Thất bại cần có giả thuyết mới từ bằng chứng trước khi retry.
