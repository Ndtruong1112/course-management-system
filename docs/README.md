# Tài Liệu Dự Án & Bộ Sưu Tập API (Documentation & Postman APIs)

Thư mục này lưu trữ tài liệu kỹ thuật, sơ đồ kiến trúc và bộ sưu tập kiểm thử API cho hệ thống Course Management System.

---

## 📁 Danh sách tệp

* `Course Management System - Full APIs.postman_collection.json`: Toàn bộ các API RESTful của hệ thống Course Management đã được cấu hình sẵn môi trường, bao gồm:
  - **Quản lý Khóa học (Courses)**: CRUD, Tìm kiếm phân trang, Lọc khoảng giá (`minPrice`, `maxPrice`).
  - **Quản lý Học viên (Students)**: CRUD, Tìm kiếm theo tên / email, Validation đầu vào.
  - **Quản lý Tài liệu & Lưu trữ (MinIO S3)**: Upload/Download tài liệu đính kèm.

---

## 🚀 Hướng dẫn Import vào Postman

1. Mở ứng dụng **Postman**.
2. Nhấn nút **Import** (góc trên bên trái).
3. Kéo thả tệp `Course Management System - Full APIs.postman_collection.json` vào Postman.
4. Chọn Collection vừa import, thiết lập biến môi trường `baseUrl`: `http://localhost:8080`.
5. Bắt đầu kiểm thử toàn diện các API.
