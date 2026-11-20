# Kiểm chứng theo phạm vi

Chạy từ gốc repository bằng PowerShell. Đây là các lựa chọn, không phải lệnh
phải chạy hết sau mỗi thay đổi. Kiểm tra script và file vẫn tồn tại trước khi dùng.

| Thay đổi | Kiểm tra phù hợp khi được yêu cầu/cho phép |
|---|---|
| Python chatbot | `python -X utf8 -m unittest discover -s chatbot/tests` |
| JS chatbot | `node --test chatbot/tests/*.cjs` |
| JS web quản lý | `node --test src/test/js/*.cjs` |
| Logic benchmark | `python -X utf8 -m unittest discover -s benchmark/tests` |
| Java một nhóm | `.\mvnw.cmd -Dtest=CourseServiceTest test` (chọn tên lớp thực tế) |
| Java đầy đủ | `.\mvnw.cmd test` |
| Python cú pháp | `python -m py_compile chatbot/web_app.py` (đổi file theo phạm vi) |
| Patch | `git diff --check` |

`MAVEN_OPTS=-Xmx384m` là mặc định cho launcher backend, không phải giới hạn của
mọi JVM con hoặc toàn bộ hệ thống. Khi cần đặt tạm trong PowerShell, dùng
`$env:MAVEN_OPTS='-Xmx384m'` trong shell công việc; không sửa cấu hình máy toàn cục.

Với giao diện Flask: render `/` bằng Flask test client, xác nhận CSS static trả
200, kiểm tra syntax script sau Jinja rendering. Khi có browser, kiểm tra
desktop/mobile, focus và mở menu/đổi mode; dùng HTTP mock cho model nếu mục
tiêu là UI. Không tuyên bố visual QA nếu chưa xem trang thực tế.

Unit test giả lập không chứng minh model load được, MySQL/MinIO đang hoạt động,
provider Cloud còn quota hoặc code sinh ra compile được. Thử GPU là bước riêng:
đo tài nguyên trước, dùng câu không chứa dữ liệu nhạy cảm, token thấp và dừng
tiến trình thử do mình tạo để trả lại RAM. Không dừng server người dùng đang dùng.

Không chạy mã output của model trực tiếp trong dự án hoặc trên database thật.
Nếu yêu cầu compile/test output, dùng workspace cô lập và kiểm tra dependency,
side effect trước khi thực thi. Lưu lệnh, exit code, lỗi và bằng chứng tương ứng.
