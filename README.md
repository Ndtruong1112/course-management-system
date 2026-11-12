# Course Management System & Local-First Hybrid Trợ Lý AI Nội Bộ

![Java](https://img.shields.io/badge/Java-21-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x%2F4.x-brightgreen.svg)
![Hibernate](https://img.shields.io/badge/Hibernate-JPA-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11-yellow.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%2012.x-red.svg)
![Model](https://img.shields.io/badge/LLM-Qwen2.5--Coder--7B%20%7C%203B-purple.svg)
![Fine-Tuning](https://img.shields.io/badge/QLoRA-4bit%20NF4%20(Colab%20%26%20Local)-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Compose%20Ready-blue.svg)

Hệ thống kết hợp toàn diện giữa **Backend Quản lý Khóa học chuẩn Doanh nghiệp** (Spring Boot 3, Java 21, Hibernate Generic DAO) và **Trợ lý Trợ Lý AI Nội Bộ "Local-First Hybrid"** được cá nhân hóa sâu sắc theo kiến trúc mã nguồn của dự án.

---

## 📌 Mục lục
- [1. Giới thiệu tổng quan](#1-giới-thiệu-tổng-quan)
- [2. Tính năng nổi bật](#2-tính-năng-nổi-bật)
- [3. Kiến trúc Hệ sinh thái Kép](#3-kiến-trúc-hệ-sinh-thái-kép)
  - [3.1. Kiến trúc Backend Java](#31-kiến-trúc-backend-java)
  - [3.2. Kiến trúc Local-First Hybrid AI](#32-kiến-trúc-local-first-hybrid-ai)
- [4. Cấu trúc thư mục toàn dự án](#4-cấu-trúc-thư-mục-toàn-dự-án)
- [5. Yêu cầu hệ thống & Cài đặt](#5-yêu-cầu-hệ-thống--cài-đặt)
- [6. Hướng dẫn Khởi chạy](#6-hướng-dẫn-khởi-chạy)
  - [6.1. Chạy Backend Spring Boot](#61-chạy-backend-spring-boot)
  - [6.2. Chạy Web Chatbot Trợ Lý AI Nội Bộ](#62-chạy-web-chatbot-ai-copilot)
  - [6.3. Chạy AI CLI trên Terminal](#63-chạy-ai-cli-trên-terminal)
- [7. Quy trình Chưng cất & Huấn luyện AI (Distillation & Fine-Tuning)](#7-quy-trình-chưng-cất--huấn-luyện-ai-distillation--fine-tuning)
- [8. Tài liệu REST API](#8-tài-liệu-rest-api)
- [9. Bảo mật & Biến môi trường](#9-bảo-mật--biến-môi-trường)
- [10. Tác giả](#10-tác-giả)

---

## 1. Giới thiệu tổng quan

Dự án gồm 2 trụ cột cốt lõi:

1. **Enterprise Course Management Backend**: Cung cấp đầy đủ các API RESTful quản lý Khóa học (Courses) và Học viên (Students), áp dụng mô hình phân lớp chuẩn, kết hợp linh hoạt giữa Spring Data JPA và mô hình **Generic DAO (Hibernate Generic DAO)**, xử lý ngoại lệ tập trung (**Global Exception Handling**) và tối ưu hóa truy vấn dữ liệu động qua **DTO Projections**.
2. **Local-First Hybrid Trợ Lý AI Nội Bộ**: Một trợ lý AI hiểu 100% ngữ cảnh kiến trúc codebase. AI Local (`Qwen2.5-Coder-3B-Instruct` được fine-tune bằng QLoRA trên GPU NVIDIA RTX 4050 6GB) đóng vai trò là "bộ não chỉ huy trung tâm":
   * **Tác vụ vừa & nhỏ** *(viết hàm DAO, câu HQL, sửa bug, giải thích code)*: Chạy trực tiếp 100% offline trên GPU cục bộ (không tốn chi phí, độ trễ thấp, bảo mật tuyệt đối).
   * **Tác vụ tổng hợp quy mô lớn** *(tạo một project mới như Khách sạn, Bệnh viện, Thư viện theo chuẩn kiến trúc của base code)*: Tự động gom cấu trúc kiến trúc dự án và ủy quyền cho Cloud AI (Google Gemini) để sinh toàn bộ source code hoàn chỉnh mà không bị thiếu hụt hay out-of-context.

---

## 2. Tính năng nổi bật

### 2.1. Nghiệp vụ Quản lý Khóa học, Sinh viên & Khoa Đào tạo
* **Quản lý Khóa học**: Xem danh sách, xem chi tiết, tạo mới, tìm kiếm theo tên (JPQL Case-insensitive), lọc theo khoảng học phí (`minPrice`, `maxPrice`).
* **Quản lý Sinh viên & Khoa trực thuộc**: Xem danh sách, thêm mới, cập nhật, xóa theo ID, tìm kiếm theo tên hoặc email, liên kết quan hệ `@ManyToOne` với Khoa đào tạo (`Department`).
* **Quản lý Khoa / Ngành Đào tạo (Department)**: Quản lý danh mục Khoa qua Generic DAO (`IDepartmentDao`, `DepartmentDaoImpl`).
* **Bảo mật & Phân quyền chuẩn Spring Security 6 + JWT**: Hỗ trợ đăng nhập, cấp phát token JWT HMAC-SHA256, phân quyền theo Role (`ADMIN`, `TEACHER`, `USER`).
* **Mô hình Generic DAO**: `IGenericDao<Pk, Entity>` và `HibernatePaginationSortingDao<Pk, Entity>` cung cấp sẵn CRUD, Transactional, Pagination, Criteria & HQL dynamic queries.
* **Cổng Quản trị Web UI Trực quan (`localhost:8080`)**: Giao diện Bootstrap 5 tích hợp sẵn Đăng nhập nhanh JWT, quản lý Khóa học, Sinh viên, Khoa và Tài liệu MinIO.
* **Khởi tạo dữ liệu mẫu tự động (`DataInitializer`) & File SQL**: Tự động sinh dữ liệu mẫu khi chạy và cung cấp script `docs/database.sql`.
* **DTO Pattern & Projections**: Tách biệt Entity CSDL và DTO truyền tải, map trực tiếp từ JPQL constructor expression (`SELECT new com.mkii...DTO(...)`).
* **Xử lý ngoại lệ tập trung**: `@RestControllerAdvice` chuẩn hóa định dạng lỗi `ErrorResponse` (timestamp, status, error, message, path).

### 2.2. Trợ lý Trợ Lý AI Nội Bộ Thông minh
* **Fine-Tuning QLoRA 4-bit**: Huấn luyện trên GPU RTX 4050, loss giảm sâu từ **1.72 xuống 0.18**, lưu trữ tại `outputs/course-management-lora-adapter`.
* **Chưng cất tri thức (Knowledge Distillation)**: Thư mục độc lập `distillation/` cho phép dùng mô hình AI lớn (Teacher Model) đọc toàn bộ 45+ file mã nguồn để sinh dataset chuyên sâu.
* **Cơ chế Router Tự động**: Phân tích ý định người dùng (User Intent) để chọn đường truyền tối ưu (Local GPU vs. Cloud Delegation).
* **Giao diện Web Hiện đại & Đấu trường So sánh (Arena)**: Web UI phong cách Tailwind CSS / Glassmorphism hỗ trợ 5 chế độ:
  1. `🧠 Trợ Lý Dự Án (Hybrid Auto)`: Tự động phân luồng Local/Cloud.
  2. `⚖️ So Sánh Model (Gốc vs Fine-tuned)`: So sánh hiệu quả của LoRA adapter trên cùng một base model.
  3. `🏆 So Sánh Hệ Thống (Dự Án vs AI Chưa Context)`: Đặt hệ thống lên bàn cân với AI phổ thông bên ngoài (zero-context).
  4. `📊 Đấu Trường 3 Chiều (Arena)`: So sánh đồng thời cả 3 thực thể trên 1 màn hình.
  5. `⚡ 100% Local GPU`: Chạy offline trên GPU NVIDIA RTX 4050.
* **Bộ Đánh Giá Kiến Trúc Tự Động (Architecture Audit Engine)**: Chấm điểm % tuân thủ 5 quy chuẩn khắt khe: Generic DAO (`HibernatePaginationSortingDao`), `EntityManager` HQL động, tránh bẫy `JpaRepository`, package `com.mkii.coursemanagementsystem`, và DTO Jakarta Validation.
* **Báo Cáo Thực Nghiệm Khoa Học**: Tự động sinh báo cáo học thuật `BAO_CAO_SO_SANH_HIEU_QUA.md` và dashboard trực quan `bao_cao_truc_quan.html` với biểu đồ Chart.js (Radar 5 chiều & Bar Chart).

---

## 3. Kiến trúc Hệ sinh thái Kép

### 3.1. Kiến trúc Backend Java

```
┌────────────────────────────────────────────────────────┐
│                   REST Controllers                     │
│         CourseRest.java  /  StudentRest.java           │
└───────────────────────────┬────────────────────────────┘
                            │ DTOs (Request / Response)
                            ▼
┌────────────────────────────────────────────────────────┐
│                    Service Layer                       │
│    CourseService / Impl  &  StudentService / Impl      │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
              ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│   Generic DAO (Hibernate) │ │ Spring Data Repository   │
│  HibernatePagination...   │ │ CourseRepository         │
│  CourseDaoImpl / Student..│ │ StudentRepository        │
└─────────────┬─────────────┘ └───────────┬──────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                 MySQL 8.0+ Database                    │
│             Bảng: courses  |  students                 │
└────────────────────────────────────────────────────────┘
```

### 3.2. Kiến trúc Local-First Hybrid AI

```
                        ┌───────────────────────────────┐
                        │          Người dùng           │
                        └──────────────┬────────────────┘
                                       │ Prompt
                                       ▼
               ┌─────────────────────────────────────────────────┐
               │    🧠 Local Brain (Qwen 3B + LoRA Adapter)      │
               │   Hiểu toàn diện: JPA, Generic DAO, DTO, HQL    │
               └───────┬─────────────────────────────────┬───────┘
                       │                                 │
           [Tác vụ vừa/nhỏ: DAO, Bug]           [Tác vụ lớn: Sinh full project]
                       │                                 │
                       ▼                                 ▼
         ┌───────────────────────────┐     ┌───────────────────────────┐
         │     ⚡ Local 3B GPU       │     │    ☁️ Cloud Sub-generator  │
         │  100% Offline, Zero cost  │     │   (Bơm đầy đủ kiến trúc   │
         │  (RTX 4050 Laptop 6GB)    │     │    để sinh toàn bộ code)  │
         └───────────────────────────┘     └───────────────────────────┘
```

---

## 4. Cấu trúc thư mục toàn dự án

```text
course-management-system/
├── start_all.bat                                   # [1-Click] Khởi động Backend (8080) và Chatbot (7860) trực tiếp
├── stop_all.bat                                    # Dừng toàn bộ tiến trình hệ thống an toàn
├── pom.xml                                         # Cấu hình Spring Boot & dependencies Maven
├── mvnw / mvnw.cmd                                 # Maven Wrapper
├── .env                                            # [Bảo mật] Lưu API Keys (đã gitignore)
├── .gitignore                                      # Loại trừ cache, adapter, venv, .env
├── docker-compose.yml                              # Cấu hình Container hóa trọn gói (MySQL, MinIO, App, AI)
├── Dockerfile                                      # Dockerfile đa tầng (Multi-stage) cho Backend
│
├── src/                                            # Mã nguồn Backend Java 21 / Spring Boot 3
│   ├── main/
│   │   ├── java/com/mkii/coursemanagementsystem/
│   │   │   ├── CourseManagementSystemApplication.java
│   │   │   ├── common/                             # Constants & Global Exception Handler
│   │   │   ├── dao/                                # Interface & Triển khai DAO
│   │   │   ├── dto/                                # Request/Response DTOs & Validation
│   │   │   ├── entity/                             # JPA Entities (Course, Student, Document)
│   │   │   ├── hibernateDao/                       # HibernatePaginationSortingDao (Generic DAO)
│   │   │   ├── repository/                         # Spring Data JPA Repositories
│   │   │   ├── rest/                               # REST Controllers
│   │   │   └── service/                            # Business Logic Layer & MinIO Storage
│   │   └── resources/
│   │       └── application.properties              # Cấu hình CSDL MySQL & MinIO S3
│   └── test/
│
├── chatbot/                                        # Hệ sinh thái Trợ Lý AI Nội Bộ & Giao diện Web
│   ├── web_app.py                                  # Web UI Flask Trợ Lý AI (SSE Streaming, Code Toolbar, 5 modes)
│   ├── run_web.bat                                 # Script khởi chạy riêng Web Chatbot (Port 7860)
│   ├── requirements.txt                            # Thư viện Python AI (Torch, Transformers, Peft...)
│   └── 2_finetuned_model/
│       └── chat.py                                 # Giao diện Chat CLI trên terminal
│
├── benchmark/                                      # Module Đánh giá Thực nghiệm Khoa học
│   ├── benchmark_comparison.py                     # Script chạy 5 kịch bản benchmark tự động
│   ├── chay_danh_gia_so_sanh.bat                   # 1-Click chạy benchmark & mở Dashboard
│   ├── BAO_CAO_SO_SANH_HIEU_QUA.md                 # Báo cáo học thuật nghiệm thu
│   ├── bao_cao_truc_quan.html                      # Bảng điều khiển trực quan (Chart.js Radar & Bar)
│   └── README.md                                   # Hướng dẫn chi tiết module benchmark
│
├── training/                                       # Module Huấn luyện & Đánh giá AI LoRA
│   ├── train_local.py                              # Huấn luyện QLoRA 4-bit (NF4) trên GPU RTX 4050
│   ├── generate_dataset.py                         # Tự động sinh tập dữ liệu từ 45+ file codebase
│   ├── test_model.py                               # Kiểm thử mô hình với ngân hàng câu hỏi
│   ├── evaluate_model.py                           # Đánh giá tỷ lệ tuân thủ kiến trúc tự động
│   ├── clean_vram.py                               # Công cụ dọn dẹp và giải phóng VRAM GPU
│   ├── dataset.jsonl                               # Tập dữ liệu Q&A kiến trúc chuẩn hóa
│   ├── eval_report.json                            # Báo cáo chi tiết kết quả đánh giá tự động
│   ├── Course_Management_AI_Colab.ipynb            # Jupyter Notebook huấn luyện trên Google Colab
│   └── README.md                                   # Hướng dẫn chi tiết pipeline huấn luyện
│
├── distillation/                                   # Module Chưng cất Tri thức (Knowledge Distillation)
│   ├── 1_export_codebase_context.py               # Quét & đóng gói mã nguồn thành markdown
│   ├── codebase_context.md                         # Toàn bộ ngữ cảnh kiến trúc dự án (45 files)
│   ├── 2_teacher_prompt.md                         # Prompt chuẩn cho AI lớn (Teacher Model)
│   ├── 3_import_distilled_data.py                  # Nhập & chuẩn hóa dữ liệu chưng cất
│   └── README.md                                   # Hướng dẫn quy trình chưng cất tri thức
│
├── docs/                                           # Tài liệu Dự án & Kiểm thử API
│   ├── Course Management System - Full APIs.postman_collection.json # Bộ Postman collection đầy đủ
│   └── README.md                                   # Hướng dẫn sử dụng & import Postman
│
└── outputs/                                        # Trọng số huấn luyện
    └── course-management-lora-adapter/             # LoRA Adapter sau khi fine-tune (Adapter weights)
```

---

## 5. Yêu cầu hệ thống & Cài đặt

### Yêu cầu phần mềm
* **Java**: JDK 21 LTS trở lên.
* **MySQL**: MySQL Server 8.0 trở lên.
* **Python**: Python 3.10 hoặc 3.11.
* **GPU (Tùy chọn cho Local AI)**: NVIDIA GPU với tối thiểu 4GB - 6GB VRAM (đã tối ưu hoàn hảo cho RTX 4050 6GB Laptop GPU). Nếu không có GPU, hệ thống tự động chạy trên CPU hoặc sử dụng Cloud backend.

### Cài đặt môi trường Python cho AI
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install transformers peft bitsandbytes datasets trl accelerate flask requests
```

---

## 6. Hướng dẫn Khởi chạy

### 6.0. Khởi chạy trọn bộ 1-Click bằng Docker Compose (Khuyên dùng nhất)

Nếu máy tính đã cài đặt **Docker Desktop**, bạn có thể khởi chạy toàn bộ hệ sinh thái (MySQL 8.0, MinIO Object Storage, Backend Spring Boot và AI Chatbot) chỉ với 1 lệnh duy nhất:

```powershell
# Khởi chạy toàn bộ hệ thống ngầm:
docker compose up -d --build

# Hoặc nhấp đúp chuột vào file tiện ích:
docker_start.bat
```

**Các cổng dịch vụ sau khi khởi chạy:**
* 🌐 **Backend Spring Boot**: `http://localhost:8080`
* 🤖 **AI Chatbot Trợ Lý AI**: `http://localhost:7860`
* 🗄️ **MinIO Web Console**: `http://localhost:9001` *(Tài khoản: `minioadmin` / Mật khẩu: `minioadmin`)*
* 📦 **MinIO S3 Storage API**: `http://localhost:9000` *(Tự động tạo sẵn bucket `documents`)*
* 🐬 **MySQL 8.0 Database**: `localhost:3306` *(CSDL: `course_db`, root password: `123456`)*

Để dừng và giải phóng tài nguyên container:
```powershell
docker compose down
# Hoặc nhấp đúp chuột vào:
docker_stop.bat
```

---

### 6.1. Chạy Backend Spring Boot (Thủ công)

1. **Cấu hình CSDL MySQL**: Mở `src/main/resources/application.properties` để kiểm tra tài khoản MySQL:
   ```properties
   spring.datasource.url=jdbc:mysql://localhost:3306/course_db?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
   spring.datasource.username=root
   spring.datasource.password=123456
   spring.jpa.hibernate.ddl-auto=update
   ```
2. **Khởi chạy ứng dụng**:
   ```powershell
   # Trên Windows:
   .\mvnw.cmd spring-boot:run
   ```
   Ứng dụng sẽ hoạt động tại: **`http://localhost:8080`**.

---

### 6.2. Chạy Web Chatbot Trợ Lý AI Nội Bộ (Khuyên dùng)

1. Đảm bảo file `.env` tại thư mục gốc có chứa API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
2. **Khởi chạy**:
   * Nhấp đúp chuột vào file: **`chatbot/run_web.bat`**
   * Hoặc mở terminal gõ:
     ```powershell
     python chatbot/web_app.py
     ```
3. Truy cập giao diện tại trình duyệt: **`http://localhost:7860`**
4. Trải nghiệm các chế độ:
   * **🧠 Trợ Lý Dự Án (Hybrid)**: Tự động nhận diện câu hỏi để điều phối giữa Local GPU và Cloud.
   * **⚖️ So Sánh Model (Gốc vs Fine-tuned)**: Chạy song song mô hình gốc (Base Qwen) và mô hình sau khi gắn adapter LoRA.
   * **🏆 So Sánh Hệ Thống (Dự Án vs AI Chưa Context)**: Đặt hệ thống lên bàn cân đối đầu với AI ngoài thị trường (Zero Context).
   * **📊 Đấu Trường 3 Chiều**: So sánh đồng thời cả 3 thực thể trên cùng 1 màn hình kèm checklist chấm điểm.
   * **⚡ 100% Local GPU**: Chạy hoàn toàn trên GPU RTX 4050 của máy, không cần internet.

---

### 6.3. Chạy AI CLI trên Terminal

Dành cho nhà phát triển muốn trao đổi trực tiếp trên dòng lệnh:
```powershell
python chatbot/2_finetuned_model/chat.py
```

---

### 6.4. Chạy Đánh giá Thực nghiệm Khoa học (Benchmark Arena)

Để chạy bộ kiểm thử khoa học 5 tình huống thực tế và tự động xuất báo cáo so sánh:
* Nhấp đúp chuột vào file: **`benchmark/chay_danh_gia_so_sanh.bat`**
* Hoặc chạy lệnh trên terminal:
  ```powershell
  python benchmark/benchmark_comparison.py
  ```
Sau khi hoàn tất, hệ thống tự động sinh 2 báo cáo nằm tại thư mục `benchmark/`:
1. **`benchmark/BAO_CAO_SO_SANH_HIEU_QUA.md`**: Báo cáo học thuật chi tiết phục vụ nghiệm thu đề tài/đồ án.
2. **`benchmark/bao_cao_truc_quan.html`**: Bảng điều khiển tương tác trực quan với biểu đồ radar 5 chiều và bar chart.
3. Hoặc xem trực tiếp qua trình duyệt web tại: **`http://localhost:7860/benchmark-report`**

---

## 7. Quy trình Chưng cất & Huấn luyện AI (Distillation & Fine-Tuning)

Dự án áp dụng trọn vẹn quy trình **Knowledge Distillation (Chưng cất tri thức)**:

```
[Mã nguồn 45 files] ──> [1_export_codebase_context.py] ──> [codebase_context.md]
                                                                  │
                                                                  ▼
[Teacher Model: Gemini/GPT-4o] <── [2_teacher_prompt.md] ─────────┘
        │
        ▼ (Sinh các cặp Q&A chuyên sâu)
[distilled_raw.json] ──> [3_import_distilled_data.py] ──> [training/dataset.jsonl]
                                                                 │
                                                                 ▼
                                                       [training/train_local.py]
                                                                 │
                                                                 ▼
                                                  [LoRA Adapter: outputs/]
```

1. **Xuất ngữ cảnh kiến trúc**:
   ```powershell
   python distillation/1_export_codebase_context.py
   ```
2. **Chưng cất dữ liệu**: Copy nội dung `codebase_context.md` và `2_teacher_prompt.md` gửi vào mô hình AI lớn để lấy dữ liệu JSON.
3. **Đóng gói dataset**:
   ```powershell
   python distillation/3_import_distilled_data.py
   ```
4. **Huấn luyện mô hình Local**:
   ```powershell
   python training/train_local.py -m 3b --steps 100
   ```
   *(Toàn bộ cache được lưu tại `D:\.cache\huggingface` để không làm đầy ổ C)*.
5. **Đánh giá Benchmark chất lượng**:
   ```powershell
   python training/evaluate_model.py
   ```
6. **Kiểm thử mô hình tương tác**:
   ```powershell
   python training/test_model.py -n 3
   ```
7. **Giải phóng VRAM GPU khi cần**:
   ```powershell
   python training/clean_vram.py
   ```

---

## 8. Tài liệu REST API

### 8.1. Quản lý Khóa học (`/api/courses`)

| Phương thức | Endpoint | Mô tả | Query Params / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/courses` | Lấy danh sách tất cả khóa học | Không |
| `GET` | `/api/courses/{id}` | Lấy chi tiết khóa học theo ID | Path `{id}` (Long) |
| `POST` | `/api/courses` | Thêm mới khóa học | JSON Body: `CourseRequestDTO` |
| `GET` | `/api/courses/search` | Tìm kiếm theo tên | `?keyword=Java` |
| `GET` | `/api/courses/filter` | Lọc theo khoảng giá | `?minPrice=100&maxPrice=500` |

#### Payload mẫu (`POST /api/courses`):
```json
{
  "title": "Lập trình Spring Boot 3 & Hibernate Chuyên Sâu",
  "description": "Khoá học thực chiến từ kiến trúc Generic DAO đến REST API",
  "duration": 60,
  "price": 499.0
}
```

---

### 8.2. Quản lý Học viên (`/api/students`)

| Phương thức | Endpoint | Mô tả | Query Params / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/students` | Lấy danh sách tất cả học viên | Không |
| `GET` | `/api/students/{id}` | Lấy chi tiết học viên theo ID | Path `{id}` (Long) |
| `POST` | `/api/students` | Thêm mới học viên | JSON Body: `StudentRequestDTO` |
| `PUT` | `/api/students/{id}` | Cập nhật thông tin học viên | Path `{id}`, JSON Body |
| `DELETE` | `/api/students/{id}` | Xóa học viên theo ID | Path `{id}` |
| `GET` | `/api/students/search` | Tìm học viên theo tên/email | `?keyword=Nguyen` |

#### Payload mẫu (`POST /api/students`):
```json
{
  "fullName": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "phone": "0987654321",
  "address": "Ha Noi, Viet Nam"
}
```

---

### 8.3. Chuẩn phản hồi lỗi (`ErrorResponse`)
Khi có ngoại lệ xảy ra, hệ thống trả về mã HTTP chuẩn cùng cấu trúc JSON:
```json
{
  "timestamp": "2026-10-23T21:40:00.123456",
  "status": 404,
  "error": "Not Found",
  "message": "Không tìm thấy khóa học với ID: 99",
  "path": "/api/courses/99"
}
```

---

### 8.4. Lệnh cURL kiểm thử nhanh

```bash
# 1. Lấy danh sách khóa học
curl -X GET http://localhost:8080/api/courses

# 2. Thêm mới học viên
curl -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Tran Thi B","email":"tranb@example.com","phone":"0912345678","address":"TP. Ho Chi Minh"}'

# 3. Lọc khóa học theo học phí
curl -X GET "http://localhost:8080/api/courses/filter?minPrice=100&maxPrice=600"
```

---

## 9. Bảo mật & Biến môi trường

* Tệp `.env` lưu trữ khóa API đã được cấu hình trong `.gitignore` để **tuyệt đối không bao giờ bị lộ hoặc tự động commit lên GitHub**.
* Dữ liệu chưng cất thô và cache mô hình nặng (`outputs/`, `D:\.cache`) đều được cách ly hoàn toàn khỏi repository Git.

---

## 10. Tác giả

* **Sinh viên / Lập trình viên**: [@MKII3184](https://github.com/MKII3184)
* **Repository**: [course-management-system-](https://github.com/MKII3184/course-management-system-)
