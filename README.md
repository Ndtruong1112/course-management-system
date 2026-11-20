# Course Management System & Local-First Hybrid Trợ Lý AI Nội Bộ

![Java](https://img.shields.io/badge/Java-21-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.1.1%20%7C%203.x-brightgreen.svg)
![Hibernate](https://img.shields.io/badge/Hibernate-Generic%20DAO-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![MinIO](https://img.shields.io/badge/MinIO-S3%20Object%20Storage-red.svg)
![Python](https://img.shields.io/badge/Python-3.11-yellow.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%2012.x-red.svg)
![LLM](https://img.shields.io/badge/LLM-Qwen2.5--Coder--3B--Instruct-purple.svg)
![Fine-Tuning](https://img.shields.io/badge/QLoRA-4bit%20NF4%20(Local%20GPU)-brightgreen.svg)
![OpenRouter](https://img.shields.io/badge/OpenRouter-DeepSeek%20V3%20Zero--Context-blue.svg)
![Antigravity](https://img.shields.io/badge/Antigravity-6%20Specialized%20Skills-success.svg)
![Docker](https://img.shields.io/badge/Docker-Compose%20Ready-blue.svg)

Hệ sinh thái tích hợp toàn diện giữa **Backend Quản lý Khóa học chuẩn Doanh nghiệp** (Spring Boot 4.1.1, Java 21, Hibernate Generic DAO, MinIO S3, bảo mật OWASP/JWT/AES fail-closed) và **Trợ lý AI Nội Bộ "Local-First Hybrid"** (Course Studio với Qwen 3B QLoRA, Codebase RAG, Intent Routing, OpenRouter DeepSeek V3 Zero-Context và bộ đánh giá 4 tiêu chí chuẩn hóa).

---

## 📌 Mục lục
- [1. Giới thiệu tổng quan](#1-giới-thiệu-tổng-quan)
- [2. Điểm nhấn Kiến trúc Doanh nghiệp (Enterprise Standards)](#2-điểm-nhấn-kiến-trúc-doanh-nghiệp-enterprise-standards)
- [3. Kiến trúc Hệ sinh thái Kép](#3-kiến-trúc-hệ-sinh-thái-kép)
  - [3.1. Kiến trúc Backend Java](#31-kiến-trúc-backend-java)
  - [3.2. Kiến trúc AI Studio Hybrid](#32-kiến-trúc-ai-studio-hybrid)
- [4. Cấu trúc thư mục toàn dự án](#4-cấu-trúc-thư-mục-toàn-dự-án)
- [5. Bộ Skill Chuyên môn Antigravity (.agents/skills)](#5-bộ-skill-chuyên-môn-antigravity-agentsskills)
- [6. Yêu cầu hệ thống & Cài đặt](#6-yêu-cầu-hệ-thống--cài-đặt)
- [7. Hướng dẫn Khởi chạy](#7-hướng-dẫn-khởi-chạy)
  - [7.1. Khởi chạy 1-Click bằng Docker Compose](#71-khởi-chạy-1-click-bằng-docker-compose)
  - [7.2. Khởi chạy nhanh bằng Scripts Windows](#72-khởi-chạy-nhanh-bằng-scripts-windows)
  - [7.3. Khởi chạy thủ công từng dịch vụ](#73-khởi-chạy-thủ-công-từng-dịch-vụ)
- [8. Trợ lý AI Course Studio & Quy trình Huấn luyện](#8-trợ-lý-ai-course-studio--quy-trình-huấn-luyện)
  - [8.1. Các chế độ hoạt động trong Course Studio](#81-các-chế-độ-hoạt-động-trong-course-studio)
  - [8.2. Hệ thống Đánh giá 4 Tiêu chí Chuẩn hóa](#82-hệ-thống-đánh-giá-4-tiêu-chí-chuẩn-hóa)
  - [8.3. Pipeline Distillation & Fine-Tuning QLoRA](#83-pipeline-distillation--fine-tuning-qlora)
- [9. Danh mục REST API & Mẫu Dữ liệu](#9-danh-mục-rest-api--mẫu-dữ-liệu)
- [10. Bảo mật & Biến môi trường](#10-bảo-mật--biến-môi-trường)
- [11. Kết quả Kiểm chứng & Độ tin cậy](#11-kết-quả-kiểm-chứng--độ-tin-cậy)
- [12. Tác giả & Giấy phép](#12-tác-giả--giấy-phép)

---

## 1. Giới thiệu tổng quan

> **Lưu ý triển khai & bảo mật:**
> - Môi trường phát triển nội bộ kích hoạt dữ liệu mẫu qua `CMS_DEMO_DATA_ENABLED=true`. Khi triển khai Production, đặt `SPRING_PROFILES_ACTIVE=prod` và cấp biến môi trường bảo mật (`SPRING_DATASOURCE_URL`, `JWT_SECRET`, `CMS_AES_KEY`, `CMS_AES_SALT`, `MINIO_*`).
> - Profile `prod` tắt tự động cập nhật schema (`ddl-auto=validate` hoặc `none`).
> - Khóa AES bảo toàn tính toàn vẹn dữ liệu: cơ chế mã hóa `AesEncryptConverter` hoạt động theo nguyên tắc **Fail-Closed** (tuyệt đối không bao giờ trả về plaintext khi lỗi mã hóa).

Dự án được cấu thành từ hai trụ cột công nghệ chính:

1. **Enterprise Course Management Backend**:
   - Kiến trúc phân tầng cô lập tuyệt đối: **REST Controller $\rightarrow$ Service Interface/Impl $\rightarrow$ Generic DAO Interface/Impl**.
   - Kế thừa cấu trúc DAO mạnh mẽ `HibernatePaginationSortingDao<Pk, Entity>` kết hợp Spring Data JPA Specification tìm kiếm đa điều kiện.
   - Quản lý tài liệu nhị phân trên **MinIO S3 Object Storage** với metadata lưu trong MySQL (`APP_DETAIL_FK`), hỗ trợ tự động Versioning và bù trừ rollback (Compensating action).
   - Truyền phát file nhị phân qua `StreamingResponseBody` không tốn RAM heap, kiểm soát phân trang an toàn (`Math.min(size, 100)`).

2. **Local-First Hybrid AI Studio (Course Studio)**:
   - Mô hình nền tảng: `Qwen2.5-Coder-3B-Instruct` kết hợp adapter QLoRA 4-bit tinh chỉnh chuyên sâu theo mã nguồn dự án.
   - Bộ định tuyến ý định thông minh (`chatbot/message_intent.py`): Tách biệt tự động giữa chào hỏi/hỏi đáp thông thường và truy vấn kỹ thuật kiến trúc để tối ưu prompt/RAG.
   - Khóa luồng an toàn `local_generation_lock`: Ngăn chặn race condition và bảo vệ VRAM RTX 4050 (6GB) khi có nhiều yêu cầu đồng thời.
   - Tích hợp đám mây linh hoạt: Google Gemini (1M context) và OpenRouter DeepSeek V3 Zero-Context.
   - Bộ đánh giá chất lượng phản hồi chuẩn hóa theo 4 tiêu chí cấp server (30/25/25/20).

---

## 2. Điểm nhấn Kiến trúc Doanh nghiệp (Enterprise Standards)

Dự án tuân thủ chặt chẽ các tiêu chuẩn kỹ thuật hàng đầu:

| Tiêu chuẩn | Điểm triển khai cụ thể trong dự án | Lợi ích đạt được |
|---|---|---|
| **Constructor Injection** *(Google/Spring Standard)* | 100% Controller và Service chuyển sang Constructor Injection với thuộc tính `private final`. | Đảm bảo tính bất biến (Immutability), loại bỏ nguy cơ phụ thuộc vòng (Circular Dependency), hỗ trợ Unit Test cô lập không cần mock runner nặng nề. |
| **Centralized Messages** *(Clean Code)* | Mọi thông báo nghiệp vụ, mã lỗi, thông báo xóa thành công tập trung tại `MessageConstants.java`. | Không hardcode chuỗi rải rác, sẵn sàng cho việc mở rộng quốc tế hóa (i18n). |
| **Graceful Shutdown** *(12-Factor / Cloud-Native)* | Cấu hình `server.shutdown=graceful` và `spring.lifecycle.timeout-per-shutdown-phase=20s`. | Cho phép hoàn tất các request HTTP và commit transaction DB dở dang khi scale down container hoặc restart service. |
| **OWASP ASVS Security Headers** | Kích hoạt `headers.frameOptions(sameOrigin)` và `contentTypeOptions()` trong `SecurityConfig.java`. | Chống tấn công Clickjacking (không bị lồng vào iframe độc hại từ domain ngoài) và chống MIME-sniffing. |
| **Streaming Zero-Copy** | Áp dụng `StreamingResponseBody` cho tải tài liệu MinIO và `StreamEvent` SSE với header `no-transform`, `X-Accel-Buffering: no`. | Tránh phình to RAM heap JVM khi tải file dung lượng lớn; chống proxy buffer làm giật luồng stream AI. |
| **Fail-Closed Cryptography** | `AesEncryptConverter` chặn hoàn toàn nguy cơ lọt dữ liệu thô ra database khi có sự cố khóa. | Dữ liệu nhạy cảm của học viên luôn được bảo vệ ở trạng thái mã hóa an toàn. |

---

## 3. Kiến trúc Hệ sinh thái Kép

### 3.1. Kiến trúc Backend Java

```
┌────────────────────────────────────────────────────────┐
│                   REST Controllers                     │
│    CourseRestImpl / StudentRestImpl / DocumentRestImpl │
└───────────────────────────┬────────────────────────────┘
                            │ Request/Response DTOs & Jakarta Validation
                            ▼
┌────────────────────────────────────────────────────────┐
│                    Service Layer                       │
│  CourseServiceImpl / StudentServiceImpl / Document... │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
              ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│   Generic DAO (Hibernate) │ │ MinIO S3 Storage Service │
│  HibernatePagination...   │ │ MinioStorageService.java │
│  CourseDaoImpl / Student..│ │ Upload/Download Stream   │
└─────────────┬─────────────┘ └───────────┬──────────────┘
              │                           │
              ▼                           ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│    MySQL 8.0+ Database    │ │   MinIO Bucket: docs     │
│ (Metadata, PII Encrypted) │ │  (Binary Object Storage) │
└───────────────────────────┘ └──────────────────────────┘
```

### 3.2. Kiến trúc AI Studio Hybrid

```
                        ┌───────────────────────────────┐
                        │      Người dùng / Studio UI   │
                        └──────────────┬────────────────┘
                                       │ POST /api/chat_stream
                                       ▼
                        ┌───────────────────────────────┐
                        │    Intent Classifier Routing  │
                        │    (chatbot/message_intent.py)│
                        └───────┬───────────────┬───────┘
                                │               │
          [Câu hỏi kiến trúc / Mã nguồn]   [Chào hỏi / Xã giao]
                                │               │
                                ▼               ▼
                 ┌──────────────────────┐ ┌─────────────┐
                 │ Codebase RAG Query   │ │ Bỏ qua RAG, │
                 │ (Trích xuất Context) │ │ Prompt gọn  │
                 └──────────────┬───────┘ └──────┬──────┘
                                └───────┬────────┘
                                        ▼
                        ┌───────────────────────────────┐
                        │  Local GPU Lock (RTX 4050)    │
                        │    local_generation_lock      │
                        └───────┬───────────────┬───────┘
                                │               │
                    [Local Mode]                [Cloud Delegated]
                                ▼                               ▼
                ┌───────────────────────────┐   ┌───────────────────────────┐
                │ Qwen 3B + LoRA Adapter    │   │ Google Gemini (1M Context)│
                │ 100% Offline, Tiết kiệm RAM│  │ DeepSeek V3 (Zero-Context)│
                └───────────────────────────┘   └───────────────────────────┘
```

---

## 4. Cấu trúc thư mục toàn dự án

```text
course-management-system/
├── pom.xml                                         # Maven build: Java 21, Spring Boot 4.1.1, MinIO, JJWT
├── mvnw / mvnw.cmd                                 # Maven Wrapper đa nền tảng
├── Dockerfile / docker-compose.yml                 # Khởi chạy full stack (MySQL, MinIO, Backend, AI)
├── .env.example                                    # Mẫu khai báo biến môi trường (Gemini, OpenRouter, DB, MinIO)
├── .gitattributes / .gitignore                     # Git LFS cấu hình cho *.safetensors & bảo vệ secrets
├── GEMINI.md                                       # Cẩm nang quy chuẩn định tuyến dành riêng cho Antigravity
│
├── .agents/skills/                                 # 6 Skill Chuyên môn Hóa cho AI Coding Agent
│   ├── cms-backend/                                # Tiêu chuẩn DAO, Service, REST, MinIO, Security
│   ├── cms-frontend/                               # Quản trị UI Admin, Course Studio, bảo vệ RAM
│   ├── cms-local-ai/                               # Vận hành Qwen LoRA, GPU lock, SSE streaming
│   ├── cms-output-evaluation/                      # Rubric 4 tiêu chí, Live review vs Benchmark
│   ├── cms-runtime-debug/                          # Script snapshot chẩn đoán tài nguyên Windows
│   └── cms-task-flow/                              # Điều phối tác vụ xuyên tầng & ma trận kiểm chứng
│
├── scripts/                                        # Bộ script vận hành Windows 1-Click
│   ├── start_local.bat / stop_local.bat            # Khởi động / Dừng trọn bộ Backend (8080) & Chatbot (7860)
│   ├── run_backend.bat / run_chatbot.bat           # Chạy riêng rẽ từng phân hệ
│   ├── docker_up.bat / docker_down.bat             # Khởi chạy stack container ngầm
│   └── run_benchmark.bat                           # Chạy kiểm định thực nghiệm và mở báo cáo
│
├── src/                                            # Mã nguồn Backend Spring Boot 4.1.1
│   ├── main/java/com/mkii/coursemanagementsystem/
│   │   ├── common/                                 # MessageConstants, ApiConstants, AES Fail-Closed Converter
│   │   ├── config/                                 # SecurityConfig (OWASP), OpenApiConfig, DataInitializer
│   │   ├── dao/                                    # Interfaces & Impls (Course, Student, Enrollment, Document...)
│   │   ├── dto/                                    # Request/Response DTOs & Jakarta Validation
│   │   ├── entity/                                 # JPA Entities: Course, Student, Department, Enrollment, Document
│   │   ├── hibernateDao/                           # Hierarchy HibernateGenericDao & HibernatePaginationSortingDao
│   │   ├── rest/                                   # REST Controllers 100% Constructor Injection
│   │   ├── service/                                # Business Logic Layer & MinioStorageService
│   │   └── specification/                          # JPA Specification Dynamic Filter Parser
│   ├── main/resources/
│   │   ├── application.properties                  # MySQL, Graceful Shutdown, Pool Hikari, MinIO, JWT
│   │   ├── application-prod.properties             # Cấu hình production nghiêm ngặt
│   │   └── static/index.html                       # Giao diện Web Quản trị Admin Dashboard
│   └── test/                                       # 81 Unit & Integration Tests (H2 isolated)
│
├── chatbot/                                        # Trợ lý AI Phân hệ Course Studio
│   ├── web_app.py                                  # Flask SSE Server (Port 7860), 4-criteria evaluation
│   ├── message_intent.py                           # Phân loại ý định tin nhắn thông minh
│   ├── rag_engine.py                               # Vectorless Codebase RAG & Semantic Matcher
│   ├── openrouter_zero.py                          # Client OpenRouter DeepSeek V3 Zero-Context
│   ├── static/studio.css                           # Giao diện CSS độc quyền Course Studio
│   └── templates/benchmark_report.html             # Báo cáo đánh giá nghiệm thu mô hình
│
├── benchmark/                                      # Đánh giá Thực nghiệm Đối chứng
│   ├── evaluate.py / evaluation_core.py            # Runner kiểm thử 4 cấu hình: Base/LoRA x Raw/RAG
│   └── cases.jsonl                                 # Bộ bài kiểm thử chuẩn hóa
│
├── distillation/                                   # Pipeline chưng cất tri thức kiến trúc dự án
│   ├── 1_export_codebase_context.py
│   ├── 2_teacher_prompt.md
│   └── 3_import_distilled_data.py
│
├── docs/                                           # Tài liệu kỹ thuật chi tiết
│   ├── ANTIGRAVITY_SKILLS.md                       # Cẩm nang hướng dẫn sử dụng bộ skill Antigravity
│   └── Course Management System - Full APIs.postman_collection.json
│
└── outputs/course-management-lora-adapter/         # Trọng số LoRA Adapter 4-bit (Git LFS)
```

---

## 5. Bộ Skill Chuyên môn Antigravity (`.agents/skills`)

Dự án tích hợp sẵn bộ **6 Agent Skills** chuyên sâu, tuân thủ nguyên tắc cách ly ngữ cảnh và kiểm chứng tối thiểu theo [GEMINI.md](file:///d:/course-management-system/GEMINI.md):

1. **`cms-task-flow`**: Định tuyến tác vụ xuyên tầng, kiểm soát luồng dữ liệu (UI $\rightarrow$ Controller $\rightarrow$ Service $\rightarrow$ DB/MinIO/AI) và tra cứu ma trận lệnh kiểm chứng tại `verification.md`.
2. **`cms-backend`**: Chuẩn hóa tầng Java, kiểm soát ràng buộc Generic DAO, constructor injection, ranh giới `@Transactional`, và xử lý bù trừ MinIO rollback.
3. **`cms-frontend`**: Duy trì API contract, quản lý streaming SSE, chống rò rỉ RAM trình duyệt, bảo vệ DOM với DOMPurify.
4. **`cms-local-ai`**: Quản lý nạp mô hình Qwen LoRA theo yêu cầu (on-demand), bảo vệ VRAM RTX 4050 và RAM 16GB, kiểm soát khóa đơn luồng `local_generation_lock`.
5. **`cms-output-evaluation`**: Quy chuẩn chấm điểm theo Rubric 4 tiêu chí (30/25/25/20), xác thực mức điểm nguyên 0–4 tại server, phân tách rạch ròi giữa Live Review và Benchmark Arena.
6. **`cms-runtime-debug`**: Chẩn đoán tức thời trạng thái RAM, working set, private commit và độ mở cổng (7860/8080) thông qua script PowerShell chỉ đọc [inspect-runtime.ps1](file:///d:/course-management-system/.agents/skills/cms-runtime-debug/scripts/inspect-runtime.ps1).

---

## 6. Yêu cầu hệ thống & Cài đặt

### Yêu cầu phần mềm
- **Java**: JDK 21 LTS trở lên (đã kiểm thử tương thích với OpenJDK 21 và OpenJDK 26).
- **MySQL**: MySQL Server 8.0+ (Cổng `3306`).
- **Python**: Python 3.10 hoặc 3.11.
- **Node.js** (Tùy chọn): Node 18+ để chạy các test case JavaScript (`.cjs`).
- **Phần cứng đề xuất cho Local AI**: NVIDIA GPU 4GB - 6GB VRAM (tối ưu hóa hoàn hảo cho RTX 4050 Laptop). Nếu không có GPU, hệ thống hỗ trợ Cloud Gemini và OpenRouter DeepSeek V3.

### Cài đặt môi trường Python
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install transformers peft bitsandbytes datasets trl accelerate flask requests
```

---

## 7. Hướng dẫn Khởi chạy

### 7.1. Khởi chạy 1-Click bằng Docker Compose

Khởi chạy đồng thời toàn bộ 4 dịch vụ (MySQL, MinIO S3, Backend Spring Boot, AI Chatbot):

```powershell
docker compose up -d --build
# Hoặc nhấp đúp: scripts\docker_up.bat
```

| Dịch vụ | URL Truy cập | Tài khoản mặc định |
|---|---|---|
| **Web Quản Trị Admin** | `http://localhost:8080` | `admin` / `admin123` |
| **AI Course Studio** | `http://localhost:7860` | Không yêu cầu |
| **MinIO Web Console** | `http://localhost:9001` | `minioadmin` / `minioadmin` |
| **MinIO S3 API** | `http://localhost:9000` | Bucket: `documents` |
| **MySQL Database** | `localhost:3306` | `root` / `123456` (DB: `course_db`) |

Dừng hệ thống container:
```powershell
docker compose down
# Hoặc nhấp đúp: scripts\docker_down.bat
```

---

### 7.2. Khởi chạy nhanh bằng Scripts Windows

Nhấp đúp vào [start_all.bat](file:///d:/course-management-system/start_all.bat) tại thư mục gốc. Script sẽ:
1. Kiểm tra cổng 8080, biên dịch và chạy Backend JAR với giới hạn RAM an toàn.
2. Kiểm tra cổng 7860 và kích hoạt AI Course Studio.
3. Tự động mở trình duyệt tại `http://localhost:7860`.

Dừng dịch vụ cục bộ: chạy [scripts/stop_local.bat](file:///d:/course-management-system/scripts/stop_local.bat).

---

### 7.3. Khởi chạy thủ công từng dịch vụ

**1. Khởi chạy Backend:**
```powershell
# Đóng gói và chạy JAR tối ưu bộ nhớ:
.\mvnw.cmd -DskipTests package
java -Xms64m -Xmx512m -jar target/course-management-system-0.0.1-SNAPSHOT.jar
```

**2. Khởi chạy Course Studio:**
```powershell
cd chatbot
python web_app.py
```

---

## 8. Trợ lý AI Course Studio & Quy trình Huấn luyện

### 8.1. Các chế độ hoạt động trong Course Studio

Truy cập `http://localhost:7860` để trải nghiệm các chế độ:
- **Trợ Lý Kỹ Thuật (Hybrid)**: Tự động phát hiện loại câu hỏi qua `message_intent.py`; định tuyến tác vụ vừa/nhỏ về Local GPU và bài toán scaffold quy mô lớn về Cloud Gemini.
- **100% Local GPU**: Chạy hoàn toàn trên GPU RTX 4050 với mô hình Qwen 3B + LoRA adapter, không gửi dữ liệu ra ngoài Internet.
- **Cloud Gemini (1M Context)**: Kết hợp RAG dự án với cửa sổ ngữ cảnh 1 triệu token của Gemini để sinh trọn vẹn toàn bộ module.
- **DeepSeek V3 (OpenRouter Cloud)**: Sử dụng mô hình DeepSeek V3 qua OpenRouter kết hợp ngữ cảnh Codebase RAG.
- **OpenRouter Zero Context**: Đối chứng mô hình DeepSeek V3 với câu hỏi thuần túy không kèm system prompt hay context dự án.
- **So Sánh Mô Hình (Base vs Fine-tuned)**: Chạy cùng lúc Base Qwen và Fine-tuned LoRA dưới cùng điều kiện phần cứng.
- **Đấu Trường 3 Chiều**: Chạy song song 3 thực thể và hiển thị scorecard đánh giá kiến trúc đồng bộ.

### 8.2. Hệ thống Đánh giá 4 Tiêu chí Chuẩn hóa

Sau mỗi phản hồi, Course Studio cung cấp tính năng **AI đề xuất điểm** dựa trên bộ Rubric 4 tiêu chí tính toán tại máy chủ:

$$\text{Điểm tiêu chí} = \left\lfloor \frac{\text{level} \times \text{max\_score} + 2}{4} \right\rfloor \quad (\text{level} \in [0..4])$$

| Tiêu chí | Trọng số tối đa | Mô tả đánh giá |
|---|:---:|---|
| **Đúng yêu cầu (Relevance)** | **30** | Trả lời đúng trọng tâm câu hỏi kỹ thuật, không lạc đề. |
| **Đầy đủ (Completeness)** | **25** | Đáp ứng trọn vẹn các thành phần (Entity, DTO, Service, DAO, Controller). |
| **Tính hợp lý (Reasoning)** | **25** | Lập luận nhất quán, đúng kiến trúc Generic DAO và nguyên tắc bảo mật. |
| **Trình bày (Clarity)** | **20** | Cấu trúc code rõ ràng, format Markdown/Java chuẩn mực. |
| **Tổng điểm** | **100** | Tổng hợp từ 4 tiêu chí trên, kèm nhận xét chi tiết. |

Người dùng có toàn quyền chỉnh sửa điểm, cập nhật nhận xét và bấm **Xác nhận đánh giá** để lưu trữ an toàn trong localStorage trình duyệt.

### 8.3. Pipeline Distillation & Fine-Tuning QLoRA

1. **Trích xuất ngữ cảnh**: `python distillation/1_export_codebase_context.py`
2. **Sinh cặp huấn luyện**: Sử dụng `distillation/2_teacher_prompt.md` qua Teacher Model.
3. **Chuẩn hóa dataset**: `python distillation/3_import_distilled_data.py`
4. **Fine-tuning QLoRA 4-bit**:
   ```powershell
   python training/train_local.py -m 3b --steps 100
   ```
5. **Đánh giá Benchmark đối chứng**:
   ```powershell
   python -X utf8 benchmark/evaluate.py run --limit 1 --max-tokens 128
   ```

---

## 9. Danh mục REST API & Mẫu Dữ liệu

Tài liệu Swagger / OpenAPI tương tác trực tiếp tại: **`http://localhost:8080/swagger-ui.html`**.

### 9.1. Quản lý Khóa học (`/api/courses`)
- `GET /api/courses`: Danh sách tất cả khóa học.
- `GET /api/courses/{id}`: Chi tiết khóa học theo ID.
- `GET /api/courses/paged?page=0&size=10&sortBy=title&sortDir=asc`: Phân trang và sắp xếp an toàn.
- `GET /api/courses/filter?minPrice=100&maxPrice=500`: Lọc theo khoảng giá.
- `POST /api/courses`: Tạo khóa học mới (Yêu cầu Role `ADMIN`, `TEACHER`, `LECTURER`).
- `PUT /api/courses/{id}`: Cập nhật khóa học.
- `DELETE /api/courses/{id}`: Xóa khóa học (Yêu cầu Role `ADMIN`).

### 9.2. Quản lý Học viên (`/api/students`)
- `GET /api/students`: Danh sách học viên (PII được mã hóa AES, yêu cầu quyền).
- `GET /api/students/search-paged?keyword=Nguyen&page=0&size=10`: Tìm kiếm phân trang.
- `POST /api/students`: Tạo hồ sơ học viên mới (Validation email, số điện thoại).

### 9.3. Quản lý Tài liệu MinIO (`/api/documents`)
- `POST /api/documents`: Tải lên danh sách file kèm `appId` (Tự động Versioning, hỗ trợ bù trừ rollback).
- `GET /api/documents/download/{id}`: Tải file qua luồng `StreamingResponseBody`.
- `POST /api/documents/delete`: Xóa mềm tài liệu (`deleted=true`, `active=false`).
- `POST /api/documents/restore/{id}`: Khôi phục tài liệu đã xóa mềm.

---

## 10. Bảo mật & Biến môi trường

Toàn bộ thông tin nhạy cảm được cấu hình thông qua biến môi trường hoặc tệp `.env`:

```env
# Cloud AI Provider Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Database Configuration
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/course_db?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=your_password

# Object Storage MinIO
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=documents

# Security Keys
JWT_SECRET=your_jwt_secret_sha256_key
CMS_AES_KEY=CourseManagementSystemSecretKey2026
CMS_AES_SALT=cms-salt-2026-v1
```

- Tệp `.env` được bảo vệ tuyệt đối trong `.gitignore`, không bao giờ được commit lên repository.
- Dữ liệu định danh cá nhân (PII) được mã hóa tự động tầng JPA bằng thuật toán AES/CBC/PKCS5Padding với Salt.

---

## 11. Kết quả Kiểm chứng & Độ tin cậy

Hệ thống được xác minh tự động định kỳ qua các bộ kiểm thử chuyên biệt:

- **Spring Boot Backend Test Suite**: `81/81 tests PASS` (Kiểm thử độc lập với cơ sở dữ liệu H2 in-memory, kiểm định toàn bộ tầng DAO, Service, REST, Security và AES Fail-Closed).
- **AI Chatbot & Intent Routing Suite**: `49/49 tests PASS` (Xác minh khả năng phân luồng câu hỏi, quản lý token, fallback zero-context).
- **Benchmark Evaluation Core**: `10/10 tests PASS` (Bảo đảm tính chính xác của công thức tính điểm và xử lý kịch bản).
- **JavaScript Web & Studio Suite**: `12/12 tests PASS` (Kiểm định cơ chế phân trang phía client, tải file luồng và chống memory leak trình duyệt).

---

## 12. Tác giả & Giấy phép

- **Tác giả**: Duy Truong ([Ndtruong1112](https://github.com/Ndtruong1112))
- **Mã nguồn dự án**: [https://github.com/Ndtruong1112/course-management-system](https://github.com/Ndtruong1112/course-management-system)
- **Giấy phép**: Phát hành theo chuẩn mã nguồn mở Apache License 2.0.
