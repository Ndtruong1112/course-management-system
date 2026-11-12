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

### 2.1. Nghiệp vụ Quản lý Khóa học, Học viên, Khoa Đào tạo & Ghi danh
* **Quản lý Khóa học (`/api/courses`)**: CRUD, phân trang phía server (`/paged`), tìm kiếm theo tên (HQL Case-insensitive), lọc theo khoảng học phí (`minPrice`, `maxPrice`).
* **Quản lý Học viên & Khoa trực thuộc (`/api/students`, `/api/departments`)**: CRUD, tìm kiếm theo tên hoặc email, liên kết `@ManyToOne` với Khoa đào tạo (`Department`), mã hóa AES-256 tầng JPA (`AesEncryptConverter`) cho dữ liệu nhạy cảm.
* **Quản lý Ghi danh (`/api/enrollments`)**: Ghi danh học viên vào khóa học, cập nhật tiến độ học tập (`progressPercent`, `status`) theo chuẩn Generic DAO (`IEnrollmentDao`, `EnrollmentDaoImpl`).
* **Thống kê & Health Check (`/api/dashboard/stats`, `/api/dashboard/health`)**: Tổng hợp KPI thời gian thực (tổng khóa học, sinh viên, khoa, lượt ghi danh, tài liệu đang hoạt động).
* **Quản lý Tài liệu & Versioning đa tầng MinIO S3 (`/api/documents`)**: Lưu file nhị phân lên MinIO, lưu metadata MySQL với khóa ngoại `APP_DETAIL_FK`, tự động đánh phiên bản (`version + 1`, bản cũ `active = false`), xóa mềm (`deleted = true`) và compensating rollback.
* **Bảo mật & Phân quyền Spring Security 6 + JWT**: Hỗ trợ đăng nhập (`/api/auth/login`), cấp token JWT HMAC-SHA256, phân quyền Role (`ADMIN`, `TEACHER`, `LECTURER`, `USER`).
* **Cổng Quản trị Web UI Trực quan (`localhost:8080`)**: Giao diện Dashboard Sidebar sáng rõ, bảng điều khiển KPI, phân trang server-side và lọc khóa học theo mức giá.

### 2.2. Course Studio — Trợ Lý AI Nội Bộ Thông minh
* **Fine-Tuning QLoRA 4-bit + RAG**: Huấn luyện `Qwen2.5-Coder-3B-Instruct` trên GPU RTX 4050 (Adapter lưu tại `outputs/course-management-lora-adapter` qua Git LFS), kết hợp `CodebaseRAG` (`chatbot/rag_engine.py`, nút `↻ RAG` làm mới nóng trên sidebar) và bộ nhớ hội thoại nhiều lượt.
* **Chưng cất tri thức (Knowledge Distillation)**: Thư mục `distillation/` cho phép trích xuất toàn bộ ngữ cảnh codebase để sinh dataset chuyên sâu.
* **Giao diện Web Studio 7 Chế độ (`http://localhost:7860`)**:
  1. `Trợ Lý Kỹ Thuật (Hybrid)`: Tự động phân luồng Local GPU vs Cloud Gemini.
  2. `100% Local GPU`: Chạy offline hoàn toàn trên GPU cục bộ.
  3. `Cloud Gemini (1M Context)`: Ủy quyền Cloud với multi-model fallback (`gemini-3-flash-preview`, `gemini-3.5-flash`, `gemini-flash-lite-latest`, `gemini-2.5-flash`).
  4. `So Sánh Mô Hình`: Base Model vs Fine-tuned + RAG ngay trên GPU.
  5. `So Sánh Hệ Thống`: Dự Án (`LoRA + RAG`) vs AI Tiêu Chuẩn (Zero Context).
  6. `Đấu Trường 3 Chiều`: Chạy tuần tự cả 3 thực thể và chấm điểm đồng bộ sau khi tất cả hoàn tất.
  7. `So Sánh Với Claude`: Đối chiếu trực tiếp với Anthropic API hoặc dán câu trả lời từ Claude.ai.
* **Bộ Đánh Giá Kiến Trúc Tự Động (`evaluate_architecture_compliance`)**: Chấm điểm đồng bộ sau khi hoàn tất phản hồi dựa trên Rubric phù hợp từng dạng bài (Module DAO, HQL Method, DTO Design, Q&A Nghiệp vụ).
* **Kết quả kiểm thử thực nghiệm**: Backend đạt **64/64 Unit Tests** (`.\mvnw test`); đánh giá 10 câu hỏi đạt **9/10 (90.00%)** với `LoRA + RAG`; Benchmark 5 kịch bản đạt **100.0%** tuân thủ kiến trúc (so với **55.0%** Base Model chưa fine-tune).

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
├── pom.xml                                         # Cấu hình Spring Boot & dependencies Maven
├── mvnw / mvnw.cmd                                 # Maven Wrapper
├── Dockerfile / docker-compose.yml                 # Container hóa trọn bộ (MySQL, MinIO, Backend, AI)
├── .env.example                                    # Mẫu cấu hình API Key & đường dẫn local model
├── .gitattributes / .gitignore                     # Git LFS cho *.safetensors & loại trừ .env, target/
│
├── scripts/                                        # Tập lệnh vận hành 1-Click trên Windows
│   ├── start_local.bat / stop_local.bat            # Khởi động/Dừng Backend (8080) & Chatbot (7860)
│   ├── docker_up.bat / docker_down.bat             # Khởi chạy/Dừng stack Docker Compose
│   ├── run_chatbot.bat                             # Chạy riêng Web Studio AI (Port 7860)
│   └── run_benchmark.bat                           # Chạy benchmark & mở Dashboard trực quan
│
├── src/                                            # Mã nguồn Backend Java 21 / Spring Boot 3
│   ├── main/java/com/mkii/coursemanagementsystem/
│   │   ├── common/                                 # Constants, Global Exception Handler, AES Converter
│   │   ├── config/                                 # Security (JWT), DataInitializer, MinIO, OpenAPI
│   │   ├── dao/                                    # Interfaces & DAO Impls (Course, Student, Enrollment, Document...)
│   │   ├── dto/                                    # Request/Response DTOs & Jakarta Validation
│   │   ├── entity/                                 # JPA Entities
│   │   ├── hibernateDao/                           # HibernateGenericDao & HibernatePaginationSortingDao
│   │   ├── rest/                                   # REST Controllers (Course, Student, Enrollment, Dashboard...)
│   │   ├── service/                                # Business Logic Layer & MinIO Storage
│   │   └── specification/                          # JPA Specification Dynamic Filtering
│   ├── main/resources/
│   │   ├── application.properties                  # Cấu hình MySQL, JWT & MinIO S3
│   │   └── static/index.html                       # Cổng quản trị Web UI (Dashboard Sidebar)
│   └── test/                                       # 64 Unit & Integration Tests
│
├── chatbot/                                        # Trợ Lý AI Nội Bộ & Course Studio Web UI
│   ├── web_app.py                                  # Flask SSE Web Studio (7 chế độ, multi-turn, đồng bộ điểm)
│   ├── rag_engine.py                               # CodebaseRAG + Bộ chấm điểm kiến trúc (Rubric-aware)
│   ├── Dockerfile / requirements.txt               # Đóng gói container & thư viện Python
│   └── 1_base_model/ , 2_finetuned_model/          # Script CLI đối chiếu Base vs Fine-tuned
│
├── training/                                       # Pipeline Huấn luyện & Đánh giá QLoRA
│   ├── generate_dataset.py / dataset.jsonl         # Sinh dữ liệu từ 95 tệp mã nguồn + docs
│   ├── train_local.py                              # QLoRA 4-bit (NF4, Attention + MLP) trên GPU 6GB
│   ├── evaluate_model.py / eval_report.json        # Đánh giá 10 câu hỏi (LoRA Only vs LoRA + RAG)
│   ├── test_model.py / clean_vram.py               # Kiểm thử nhanh & giải phóng VRAM
│   └── Course_Management_AI_Colab.ipynb            # Notebook huấn luyện trên Colab
│
├── benchmark/                                      # Kiểm thử Thực nghiệm 5 Kịch bản (TC-01..TC-05)
│   ├── benchmark_comparison.py                     # So sánh External Zero-Context, Base GPU, Project LoRA+RAG
│   ├── BAO_CAO_SO_SANH_HIEU_QUA.md                 # Báo cáo nghiệm thu Markdown
│   └── bao_cao_truc_quan.html                      # Dashboard Chart.js (Radar & Bar)
│
├── distillation/                                   # Chưng cất Tri thức từ Teacher Model
│   ├── 1_export_codebase_context.py                # Đóng gói ngữ cảnh codebase
│   ├── 2_teacher_prompt.md                         # Prompt sinh dữ liệu cho Teacher LLM
│   └── 3_import_distilled_data.py                  # Chuẩn hóa vào training/dataset.jsonl
│
├── docs/                                           # Tài liệu API, CSDL & Lịch sử rà soát
│   ├── Course Management System - Full APIs.postman_collection.json
│   ├── openapi.json / database.sql / BAO_CAO_LOI.md
│   └── README.md
│
└── outputs/course-management-lora-adapter/         # Trọng số LoRA Adapter chính thức (Git LFS)
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
scripts\docker_up.bat
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
scripts\docker_down.bat
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
   * Nhấp đúp chuột vào file: **`scripts/run_chatbot.bat`** (hoặc chạy trọn bộ Backend + AI qua **`scripts/start_local.bat`**)
   * Hoặc mở terminal gõ:
     ```powershell
     python chatbot/web_app.py
     ```
3. Truy cập giao diện tại trình duyệt: **`http://localhost:7860`**
4. Trải nghiệm 7 chế độ trên Course Studio:
   * **Trợ Lý Kỹ Thuật (Hybrid)**: Tự động nhận diện câu hỏi để điều phối giữa Local GPU và Cloud Gemini.
   * **100% Local GPU**: Chạy hoàn toàn trên GPU RTX 4050 của máy, không cần internet.
   * **Cloud Gemini (1M Context)**: Sinh mã nguồn lớn với context codebase + multi-model fallback.
   * **So Sánh Mô Hình (Base vs Fine-tuned)**: Chạy song song mô hình gốc và mô hình sau khi gắn adapter LoRA.
   * **So Sánh Hệ Thống (Dự Án vs AI Tiêu Chuẩn)**: Đối chiếu hệ thống dự án với AI phổ thông bên ngoài (Zero Context).
   * **Đấu Trường 3 Chiều**: So sánh đồng thời 3 luồng kèm chấm điểm đồng bộ sau khi cả 3 hoàn tất.
   * **So Sánh Với Claude**: Đối chiếu trực tiếp qua Anthropic API hoặc dán câu trả lời từ Claude.ai.

---

### 6.3. Chạy AI CLI trên Terminal

Dành cho nhà phát triển muốn trao đổi trực tiếp trên dòng lệnh:
```powershell
python chatbot/2_finetuned_model/chat.py
```

---

### 6.4. Chạy Đánh giá Thực nghiệm Khoa học (Benchmark Arena)

Để chạy bộ kiểm thử khoa học 5 tình huống thực tế và tự động xuất báo cáo so sánh:
* Nhấp đúp chuột vào file: **`scripts/run_benchmark.bat`**
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

## 10. Tác giả & Repository

* **GitHub Repository**: [Ndtruong1112/course-management-system](https://github.com/Ndtruong1112/course-management-system)
