# Tài Liệu Dự Án & Bộ Sưu Tập API (Documentation & Postman APIs)

Thư mục này lưu trữ tài liệu kỹ thuật, sơ đồ kiến trúc và bộ sưu tập kiểm thử API cho hệ thống Course Management System.

---

## 📁 Danh sách tệp

* `Course Management System - Full APIs.postman_collection.json`: Toàn bộ các API RESTful của hệ thống Course Management (Courses, Students, Departments, Enrollments, Documents MinIO, Dashboard, Auth JWT).
* `openapi.json`: Đặc tả OpenAPI 3.0 cho toàn bộ endpoint REST.
* `database.sql`: Script khởi tạo lược đồ cơ sở dữ liệu MySQL mẫu.
* `BAO_CAO_LOI.md`: Tài liệu lưu trữ đợt rà soát hệ thống lịch sử (2026-10-31).

---

## 🚀 Hướng dẫn Import vào Postman

1. Mở ứng dụng **Postman**.
2. Nhấn nút **Import** (góc trên bên trái).
3. Kéo thả tệp `Course Management System - Full APIs.postman_collection.json` vào Postman.
4. Chọn Collection vừa import, thiết lập biến môi trường `baseUrl`: `http://localhost:8080`.
5. Bắt đầu kiểm thử toàn diện các API.
