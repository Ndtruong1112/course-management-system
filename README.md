# Course Management System (Spring Boot REST API)

![Java](https://img.shields.io/badge/Java-21-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.1.1-brightgreen.svg)
![Hibernate](https://img.shields.io/badge/Hibernate-JPA-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![Maven](https://img.shields.io/badge/Maven-Build-red.svg)

Hệ thống quản lý khóa học (Course Management System) là một ứng dụng backend được xây dựng bằng **Spring Boot** và **Java 21**, cung cấp các dịch vụ **RESTful API** để quản lý thông tin Khóa học (Courses) và Học viên (Students). 

Dự án áp dụng mô hình kiến trúc phân lớp chuẩn Enterprise, kết hợp linh hoạt giữa **Spring Data JPA Repository** và mô hình **Generic DAO (Hibernate Generic DAO)**, triển khai **DTO Pattern**, xử lý truy vấn động/tùy chỉnh (**JPQL Custom Queries & DTO Projections**) và cơ chế xử lý ngoại lệ tập trung (**Global Exception Handling**).

---

## 📌 Mục lục
- [Tính năng nổi bật](#-tính-năng-nổi-bật)
- [Kiến trúc và Công nghệ](#-kiến-trúc-và-công-nghệ)
- [Cấu trúc thư mục dự án](#-cấu-trúc-thư-mục-dự-án)
- [Yêu cầu hệ thống & Cài đặt](#-yêu-cầu-hệ-thống--cài-đặt)
- [Cấu hình cơ sở dữ liệu](#-cấu-hình-cơ-sở-dữ-liệu)
- [Tài liệu REST API](#-tài-liệu-rest-api)
  - [1. Quản lý Khóa học (Courses)](#1-quản-lý-khóa-học-courses)
  - [2. Quản lý Học viên (Students)](#2-quản-lý-học-viên-students)
  - [3. Xử lý lỗi & Định dạng phản hồi lỗi](#3-xử-lý-lỗi--định-dạng-phản-hồi-lỗi)
- [Hướng dẫn kiểm thử API](#-hướng-dẫn-kiểm-thử-api)
- [Tác giả](#-tác-giả)

---

## 🚀 Tính năng nổi bật

- **Quản lý Khóa học (Course Management)**:
  - Xem danh sách tất cả các khóa học.
  - Xem chi tiết khóa học theo ID.
  - Thêm mới khóa học thông qua Hibernate Generic DAO.
  - Tìm kiếm khóa học theo từ khóa tiêu đề (Search by Title - Case-insensitive JPQL).
  - Lọc khóa học theo khoảng học phí (Filter by Price Range JPQL).

- **Quản lý Học viên (Student Management)**:
  - Xem danh sách tất cả học viên.
  - Xem chi tiết thông tin học viên theo ID.
  - Đăng ký học viên mới qua DAO layer.
  - Cập nhật thông tin học viên (Họ tên, email, số điện thoại, địa chỉ).
  - Xóa học viên theo ID.
  - Tìm kiếm học viên theo tên hoặc email.

- **Thiết kế kiến trúc nâng cao**:
  - **Mô hình Generic DAO**: `IGenericDao<Pk, Entity>` và `HibernateGenericDao<Pk, Entity>` kế thừa từ `SimpleJpaRepository`, cung cấp sẵn các thao tác CRUD, Transactional, Pagination, HQL/JPQL helper methods.
  - **DTO Pattern & Projections**: Tách biệt giữa Entity lưu trữ database và Data Transfer Object (RequestDTO, ResponseDTO) giúp bảo mật, tối ưu dữ liệu truyền tải và map trực tiếp dữ liệu từ câu lệnh JPQL constructor expression (`SELECT new com.mkii...DTO(...)`).
  - **Global Exception Handling**: Sử dụng `@RestControllerAdvice` và `@ExceptionHandler` bắt và chuẩn hóa các lỗi (`ResourceNotFoundException`, `BadRequestException`, `IllegalArgumentException`, `Exception`).
  - **Quản lý Hằng số tập trung**: Tách biệt `ApiConstants` (quản lý đường dẫn Endpoint) và `MessageConstants` (quản lý thông báo lỗi hệ thống).

---

## 🛠 Kiến trúc và Công nghệ

- **Ngôn ngữ**: Java 21 LTS
- **Framework**: Spring Boot 4.x / 3.x (Spring Web MVC, Spring Data JPA)
- **ORM / Persistence**: Hibernate, Jakarta Persistence (JPA)
- **Database**: MySQL 8.x
- **Build Tool**: Apache Maven (kèm Maven Wrapper `mvnw` & `mvnw.cmd`)
- **Thư viện hỗ trợ**:
  - `Lombok`: Tự động sinh getter/setter, builder, constructor giúp code ngắn gọn.
  - `mysql-connector-j`: MySQL JDBC Driver.

---

## 📂 Cấu trúc thư mục dự án

```text
course-management-system/
├── pom.xml                                         # Cấu hình dependencies Maven
├── mvnw / mvnw.cmd                                 # Maven Wrapper
└── src/
    ├── main/
    │   ├── java/com/mkii/coursemanagementsystem/
    │   │   ├── CourseManagementSystemApplication.java # Class khởi chạy Spring Boot
    │   │   ├── common/                             # Định nghĩa constants & exceptions
    │   │   │   ├── ApiConstants.java               # URL Endpoints
    │   │   │   ├── MessageConstants.java           # Chuỗi thông báo hệ thống
    │   │   │   └── exception/                      # Global Exception Handlers & DTO
    │   │   │       ├── BadRequestException.java
    │   │   │       ├── ErrorResponse.java
    │   │   │       ├── GlobalExceptionHandler.java
    │   │   │       └── ResourceNotFoundException.java
    │   │   ├── dao/                                # Data Access Object interfaces
    │   │   │   ├── IGenericDao.java
    │   │   │   ├── CourseDao.java
    │   │   │   ├── StudentDao.java
    │   │   │   └── impl/                           # Triển khai DAO
    │   │   │       ├── CourseDaoImpl.java
    │   │   │       └── StudentDaoImpl.java
    │   │   ├── dto/                                # Data Transfer Objects
    │   │   │   ├── CourseRequestDTO.java
    │   │   │   ├── CourseResponseDTO.java
    │   │   │   ├── StudentRequestDTO.java
    │   │   │   └── StudentResponseDTO.java
    │   │   ├── entity/                             # JPA Entities ánh xạ database
    │   │   │   ├── Course.java
    │   │   │   └── Student.java
    │   │   ├── hibernateDao/                       # Lớp base Generic DAO với Hibernate/JPA
    │   │   │   └── HibernateGenericDao.java
    │   │   ├── repository/                         # Spring Data JPA Repositories
    │   │   │   ├── CourseRepository.java
    │   │   │   └── StudentRepository.java
    │   │   ├── rest/                               # REST Controllers
    │   │   │   ├── CourseRest.java
    │   │   │   └── StudentRest.java
    │   │   └── service/                            # Business Logic Layer
    │   │       ├── CourseService.java
    │   │       ├── CourseServiceImpl.java
    │   │       ├── StudentService.java
    │   │       └── StudentServiceImpl.java
    │   └── resources/
    │       └── application.properties              # Cấu hình datasource & Hibernate
    └── test/
        └── java/com/mkii/coursemanagementsystem/
            └── CourseManagementSystemApplicationTests.java
```

---

## ⚙️ Yêu cầu hệ thống & Cài đặt

### 1. Yêu cầu môi trường
- **JDK**: Java Development Kit 21 trở lên.
- **MySQL**: Phiên bản 8.0 trở lên đang chạy (port mặc định `3306`).
- **Maven**: Phiên bản 3.8+ (hoặc dùng trực tiếp `./mvnw` đi kèm dự án).

### 2. Cài đặt và chạy ứng dụng

1. **Clone repository**:
   ```bash
   git clone https://github.com/MKII3184/course-management-system-.git
   cd course-management-system-
   ```

2. **Cấu hình Database**:
   Mở file `src/main/resources/application.properties` và điều chỉnh thông tin kết nối MySQL nếu cần:
   ```properties
   spring.datasource.url=jdbc:mysql://localhost:3306/course_db?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
   spring.datasource.username=root
   spring.datasource.password=dmcvmkii28
   spring.jpa.hibernate.ddl-auto=update
   spring.jpa.show-sql=true
   spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
   ```
   > **Lưu ý**: Cờ `createDatabaseIfNotExist=true` sẽ tự động tạo database `course_db` trên MySQL nếu chưa tồn tại.

3. **Biên dịch và Chạy ứng dụng**:
   - Sử dụng Maven Wrapper:
     ```bash
     # Trên Windows:
     .\mvnw.cmd spring-boot:run

     # Trên Linux/macOS:
     chmod +x mvnw
     ./mvnw spring-boot:run
     ```
   - Ứng dụng sẽ khởi động tại: `http://localhost:8080`

---

## 📡 Tài liệu REST API

### 1. Quản lý Khóa học (Courses)
Đường dẫn gốc: `/api/courses`

| Phương thức | Endpoint | Mô tả | Query Params / Request Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses` | Lấy danh sách tất cả các khóa học | Không |
| `GET` | `/api/courses/{id}` | Lấy thông tin chi tiết một khóa học theo ID | Đường dẫn `{id}` (Long) |
| `POST` | `/api/courses` | Tạo mới một khóa học | JSON Body: `CourseRequestDTO` |
| `GET` | `/api/courses/search` | Tìm kiếm khóa học theo tên | `?keyword=Java` |
| `GET` | `/api/courses/filter` | Lọc khóa học theo khoảng giá | `?minPrice=100&maxPrice=500` |

#### Payload mẫu khi tạo Khóa học (`POST /api/courses`):
```json
{
  "title": "Lập trình Java và Spring Boot Chuyên Sâu",
  "description": "Khóa học từ cơ bản đến nâng cao về REST API và Spring Boot",
  "duration": 45,
  "price": 299.99
}
```

#### Phản hồi mẫu (`200 OK`):
```json
{
  "id": 1,
  "title": "Lập trình Java và Spring Boot Chuyên Sâu",
  "description": "Khóa học từ cơ bản đến nâng cao về REST API và Spring Boot",
  "duration": 45,
  "price": 299.99
}
```

---

### 2. Quản lý Học viên (Students)
Đường dẫn gốc: `/api/students`

| Phương thức | Endpoint | Mô tả | Query Params / Request Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/students` | Lấy danh sách tất cả học viên | Không |
| `GET` | `/api/students/{id}` | Lấy chi tiết thông tin học viên theo ID | Đường dẫn `{id}` (Long) |
| `POST` | `/api/students` | Thêm mới một học viên | JSON Body: `StudentRequestDTO` |
| `PUT` | `/api/students/{id}` | Cập nhật thông tin học viên theo ID | Đường dẫn `{id}`, JSON Body |
| `DELETE` | `/api/students/{id}` | Xóa học viên theo ID | Đường dẫn `{id}` |
| `GET` | `/api/students/search` | Tìm kiếm học viên theo tên hoặc email | `?keyword=Nguyen` |

#### Payload mẫu khi tạo Học viên (`POST /api/students`):
```json
{
  "fullName": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "phone": "0987654321",
  "address": "Ha Noi, Viet Nam"
}
```

#### Phản hồi mẫu (`201 CREATED`):
```json
{
  "id": 1,
  "fullName": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "phone": "0987654321",
  "address": "Ha Noi, Viet Nam"
}
```

---

### 3. Xử lý lỗi & Định dạng phản hồi lỗi
Khi có lỗi xảy ra (ví dụ: không tìm thấy tài nguyên, dữ liệu không hợp lệ), `GlobalExceptionHandler` sẽ trả về mã trạng thái HTTP tương ứng cùng cấu trúc chuẩn JSON `ErrorResponse`:

```json
{
  "timestamp": "2026-09-19T17:00:00.123456",
  "status": 404,
  "error": "Not Found",
  "message": "Không tìm thấy khóa học với ID: 99",
  "path": "/api/courses/99"
}
```

---

## 🧪 Hướng dẫn kiểm thử API (cURL Examples)

#### 1. Tạo mới một khóa học:
```bash
curl -X POST http://localhost:8080/api/courses \
  -H "Content-Type: application/json" \
  -d '{"title":"Spring Boot Mastery","description":"Học Spring Boot thực chiến","duration":30,"price":199.0}'
```

#### 2. Lấy danh sách khóa học:
```bash
curl -X GET http://localhost:8080/api/courses
```

#### 3. Tìm kiếm khóa học theo từ khóa:
```bash
curl -X GET "http://localhost:8080/api/courses/search?keyword=Spring"
```

#### 4. Thêm mới một học viên:
```bash
curl -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Tran Thi B","email":"tranb@example.com","phone":"0912345678","address":"TP. Ho Chi Minh"}'
```

#### 5. Cập nhật học viên:
```bash
curl -X PUT http://localhost:8080/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Tran Thi B (Cap nhat)","email":"tranb_updated@example.com","phone":"0912345678","address":"Da Nang"}'
```

#### 6. Xóa học viên:
```bash
curl -X DELETE http://localhost:8080/api/students/1
```

---

## 🤖 Bộ công cụ AI Fine-Tuning & Benchmark độc lập

Dự án tích hợp trọn gói chu trình AI cá nhân hóa (QLoRA 4-bit) dành riêng cho kiến trúc Course Management System:

1. **Sinh dữ liệu huấn luyện (`generate_dataset.py`)**:
   - Quét toàn bộ 51+ tệp mã nguồn Java, Properties, XML, Postman collection.
   - Sinh các cặp câu hỏi - câu trả lời chi tiết về nghiệp vụ khóa học, học viên, phân tầng DAO, lưu trữ MinIO và cơ chế versioning.
   - Lệnh chạy:
     ```bash
     py -3.11 generate_dataset.py
     ```
   - Xuất file: `dataset.jsonl` (111+ mẫu dữ liệu hội thoại chuẩn ChatML).

2. **Huấn luyện mô hình cục bộ (`train_local.py`)**:
   - Sử dụng mô hình nền tảng: `Qwen/Qwen2.5-Coder-1.5B-Instruct`.
   - Cơ chế tối ưu: Lượng tử hóa 4-bit NF4 kết hợp LoRA (QLoRA) với bộ tối ưu `paged_adamw_8bit`, tương thích hoàn hảo GPU laptop RTX 4050 6GB VRAM.
   - Lệnh chạy:
     ```bash
     py -3.11 train_local.py
     ```
   - Đầu ra: Trọng số LoRA Adapter lưu tại thư mục `outputs/course-management-lora-adapter`.

3. **Kiểm thử đối thoại trực tiếp (`test_model.py`)**:
   - Nạp mô hình đã fine-tuned và đặt các câu hỏi kỹ thuật về mã nguồn dự án.
   - Lệnh chạy:
     ```bash
     py -3.11 test_model.py
     ```

4. **Bộ kiểm thử Benchmark độ chính xác độc lập (`evaluate_model.py`)**:
   - Chứa tập câu hỏi đánh giá độc lập (Test Set) bao quát 10 khía cạnh: Database, Foreign Keys, Versioning, Soft Delete, MinIO, Generic DAO, Entities, HQL, Constraints, API Endpoints.
   - Tự động chấm điểm (Pass/Fail) và tính toán tỷ lệ chính xác (Accuracy %).
   - Lệnh chạy:
     ```bash
     py -3.11 evaluate_model.py
     ```
   - Xuất báo cáo chi tiết: `eval_report.json`.

---

## 👤 Tác giả
- GitHub: [@MKII3184](https://github.com/MKII3184)
- Repository: [course-management-system-](https://github.com/MKII3184/course-management-system-)
