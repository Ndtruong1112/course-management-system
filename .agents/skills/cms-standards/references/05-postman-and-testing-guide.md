# Hướng dẫn Postman & Quy chuẩn kiểm thử (Postman & Testing Guide)

Tài liệu này cung cấp danh mục 49 API trong Postman Collection, biến môi trường, hướng dẫn thiết lập môi trường chạy thử và các lệnh kiểm thử tự động (Unit Test).

---

## 1. Postman Collection Overview

File Postman collection chính nằm tại:
`C:\Users\24110\Downloads\Course Management System - Full APIs.postman_collection.json`
(Đã đồng bộ một bản tại thư mục gốc của project).

### Thống kê tổng số 49 API:
* **Courses:** 18 requests
* **Students:** 17 requests
* **Documents (MinIO Storage):** 14 requests

---

## 2. Chi tiết danh mục API theo Module

### A. Courses (18 Requests)
1. `GET /api/courses` : Lấy tất cả khóa học
2. `GET /api/courses/{id}` : Lấy chi tiết khóa học theo ID
3. `POST /api/courses` : Thêm mới khóa học
4. `POST /api/courses/batch` : Thêm hàng loạt khóa học (`createAll`)
5. `PUT /api/courses/{id}` : Cập nhật khóa học
6. `DELETE /api/courses/{id}` : Xóa khóa học theo ID
7. `GET /api/courses/search?title=...` : Tìm kiếm theo tên (qua `findByHql`)
8. `GET /api/courses/filter?minPrice=...&maxPrice=...` : Lọc theo học phí (qua `findByHql`)
9. `GET /api/courses/by-title?title=...` : Lấy khóa học theo tiêu đề chính xác
10. `GET /api/courses/by-field?fieldName=...&value=...` : Lấy 1 bản ghi theo trường động (`getByField`)
11. `GET /api/courses/by-field-list?fieldName=...&value=...` : Lấy danh sách nhiều bản ghi theo trường động (`findByField`)
12. `GET /api/courses/by-field-paged?fieldName=...&value=...&page=0&size=5` : Phân trang & sắp xếp theo trường động
13. `GET /api/courses/spec-search?search=title:Spring,price>500000` : Tìm kiếm đa điều kiện JPA Specification
14. `GET /api/courses/sorted?sortBy=price&direction=desc` : Lấy tất cả có sắp xếp (`findAllSorted`)
15. `GET /api/courses/paged?page=0&size=5&sortBy=title&direction=asc` : Phân trang & sắp xếp (`findAllPaged`)
16. `GET /api/courses/spec-search-sorted?search=...&sortBy=...&direction=...` : Specification + Sắp xếp
17. `GET /api/courses/spec-search-paged?search=...&page=0&size=5&sortBy=...` : Specification + Phân trang + Sắp xếp
18. `GET /api/courses/count` : Đếm tổng số lượng khóa học

### B. Students (17 Requests)
1. `GET /api/students` : Lấy tất cả sinh viên
2. `GET /api/students/{id}` : Lấy chi tiết sinh viên theo ID
3. `POST /api/students` : Thêm mới sinh viên
4. `POST /api/students/batch` : Thêm hàng loạt sinh viên (`createAll`)
5. `PUT /api/students/{id}` : Cập nhật sinh viên
6. `DELETE /api/students/{id}` : Xóa sinh viên theo ID
7. `GET /api/students/search?name=...` : Tìm kiếm theo họ tên (qua `findByHql`)
8. `GET /api/students/by-email?email=...` : Lấy sinh viên theo email
9. `GET /api/students/by-field?fieldName=...&value=...` : Lấy 1 bản ghi theo trường động
10. `GET /api/students/by-field-list?fieldName=...&value=...` : Lấy danh sách theo trường động
11. `GET /api/students/by-field-paged?fieldName=...&value=...&page=0&size=5` : Phân trang theo trường động
12. `GET /api/students/spec-search?search=fullName:Nguyen,address:Hanoi` : Tìm kiếm đa điều kiện JPA Specification
13. `GET /api/students/sorted?sortBy=fullName&direction=asc` : Sắp xếp danh sách
14. `GET /api/students/paged?page=0&size=5&sortBy=fullName&direction=asc` : Phân trang danh sách
15. `GET /api/students/spec-search-sorted?search=...&sortBy=...` : Specification + Sắp xếp
16. `GET /api/students/spec-search-paged?search=...&page=0&size=5` : Specification + Phân trang + Sắp xếp
17. `GET /api/students/count` : Đếm tổng số lượng sinh viên

### C. Documents (14 Requests)
1. `POST /api/documents/create` : Tải lên tài liệu kèm nghiệp vụ (`appId`, multipart `files`)
2. `GET /api/documents/download/{id}` : Tải về tài liệu theo Document ID
3. `GET /api/documents/download?filePath=...` : Tải về theo filePath MinIO
4. `POST /api/documents/delete` : Xóa mềm qua body JSON `{"id": "..."}`
5. `DELETE /api/documents/{id}` : Xóa mềm theo Path ID
6. `GET /api/documents/{id}` : Lấy chi tiết tài liệu theo ID
7. `GET /api/documents/app/{appId}` : Lấy danh sách tài liệu theo mã nghiệp vụ `appId`
8. `GET /api/documents` (hoặc `/list`) : Lấy tất cả tài liệu active
9. `GET /api/documents/search?query=...&lowerLimit=0&upperLimit=10&orderBy=...&appId=...` : Tìm kiếm & phân trang kết hợp
10. `GET /api/documents/count?query=...&appId=...` : Đếm số lượng tài liệu
11. `GET /api/documents/paged?page=0&size=10&sortBy=creationTime&direction=desc` : Phân trang toàn bộ tài liệu (`findAllPaged`)
12. `GET /api/documents/sorted?sortBy=name&direction=asc` : Sắp xếp toàn bộ tài liệu (`findAllSorted`)
13. `GET /api/documents/app/{appId}/paged?page=0&size=10` : Phân trang tài liệu theo appId (`findByFieldPaged`)
14. `GET /api/documents/spec-search-paged?search=name:tai_lieu&page=0&size=10` : Specification + Phân trang

---

## 3. Cấu hình Biến môi trường Postman

* **Variable Name:** `baseUrl`
* **Initial Value:** `http://localhost:8080`
* **Current Value:** `http://localhost:8080`

Khi tạo tài liệu mới thành công, sao chép giá trị `id` trả về để gán vào biến `{{docId}}` trong Postman nhằm test nhanh các API download và xóa.

---

## 4. Chạy kiểm thử tự động (Unit Test Execution)

### Lưu ý quan trọng về phiên bản JDK:
Dự án được cấu hình cho **Java 21+**. Nếu chạy trên PowerShell mặc định nhận Java 8 (class file version 52.0), Maven Surefire sẽ báo lỗi `UnsupportedClassVersionError: org/junit/platform/launcher/TagFilter has been compiled by a more recent version (61.0)`.

### Lệnh chạy chuẩn (gán đúng JAVA_HOME trước khi test):
```bat
cmd /c "set JAVA_HOME=C:\Users\24110\.jdks\openjdk-26.0.2.1 && set PATH=C:\Users\24110\.jdks\openjdk-26.0.2.1\bin;%PATH% && mvnw.cmd test -Dtest=DocumentServiceTest"
```

### Chạy toàn bộ test trong project:
```bat
cmd /c "set JAVA_HOME=C:\Users\24110\.jdks\openjdk-26.0.2.1 && set PATH=C:\Users\24110\.jdks\openjdk-26.0.2.1\bin;%PATH% && mvnw.cmd test"
```
