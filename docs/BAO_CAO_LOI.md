# BÁO CÁO RÀ SOÁT LỖI - COURSE MANAGEMENT SYSTEM

- **Ngày rà soát:** 2026-10-31
- **Phạm vi:** Backend Spring Boot (`src/main/java`), cấu hình, UI tĩnh (`static/index.html`), Postman collection, Docker Compose/Dockerfile, chatbot Python.
- **Nguyên tắc:** Chỉ báo cáo, **chưa sửa bất kỳ file mã nguồn nào**.
- **Mức độ:** 🔴 Nghiêm trọng (phải sửa sớm) · 🟠 Chức năng (đã xác nhận lỗi) · 🟡 Trung bình (chất lượng/bảo mật/vận hành) · 🔵 Thấp (cosmetic, tài liệu)

---

## 1. Kết quả kiểm chứng tự động

| Hạng mục | Lệnh | Kết quả |
|---|---|---|
| Biên dịch | `.\mvnw.cmd -B -DskipTests compile` | **BUILD SUCCESS** (85 source files) |
| Kiểm thử | `.\mvnw.cmd -B test` | **45/45 test pass**, 0 failure, 0 error |
| Spring context | `CourseManagementSystemApplicationTests` | Pass (7.09s) |

> Kết luận: các lỗi bên dưới **không phải lỗi biên dịch**, mà là lỗi logic, bảo mật và cấu hình chỉ xuất hiện khi chạy thực tế hoặc khi client gọi đúng/sai cách.

---

## 2. Tổng hợp số lượng

| Mức độ | Số lượng |
|---|---|
| 🔴 Nghiêm trọng | 6 |
| 🟠 Chức năng | 9 |
| 🟡 Trung bình | 8 (bảo mật/kiến trúc) + 7 (vận hành/tài liệu) |
| 🔵 Thấp | 4 |

---

## 3. 🔴 LỖI NGHIÊM TRỌNG

### A1. `/api/documents/search` luôn lỗi 500 do sai alias JPQL

- **Vị trí:**
  - `src/main/java/com/mkii/coursemanagementsystem/dao/impl/DocumentDaoImpl.java:125-126`
  - `src/main/java/com/mkii/coursemanagementsystem/hibernateDao/HibernatePaginationSortingDao.java:183-199`
- **Nguyên nhân:** `getDoc()` tạo JPQL `SELECT d FROM Document d ...` (alias `d`) nhưng gọi `buildOrderClause(sort)`; hàm này hardcode tiền tố `e.` → `ORDER BY e.creationTime DESC`.
- **Ảnh hưởng:** Endpoint `GET /api/documents/search` (và mọi API gọi `getDoc`) ném `SemanticException`/`QueryException` → HTTP 500. Mặc định `orderBy=creationTime` nên gần như luôn lỗi.
- **Hướng khắc phục:** Cho `buildOrderClause` nhận alias, hoặc dùng alias `e` thống nhất toàn bộ truy vấn trong `getDoc`.

### A2. Leo thang đặc quyền qua API đăng ký công khai

- **Vị trí:** `rest/impl/AuthRestImpl.java:82-92`, `dto/auth/RegisterRequest.java:28`
- **Nguyên nhân:** `role` lấy trực tiếp từ request, chỉ `trim().toUpperCase()`, không whitelist.
- **Ảnh hưởng:** Bất kỳ ai cũng gọi `POST /api/auth/register` với `"role": "ADMIN"` để tạo tài khoản quản trị.
- **Hướng khắc phục:** Luôn gán `USER` khi tự đăng ký; cấp `ADMIN/TEACHER` qua API quản trị có `@PreAuthorize` riêng.

### A3. Lộ dữ liệu cá nhân và tài liệu qua GET công khai

- **Vị trí:** `config/SecurityConfig.java:102`, `rest/DocumentRest.java:19-23`
- **Nguyên nhân:** `.requestMatchers(HttpMethod.GET, "/api/courses/**", "/api/students/**", "/api/departments/**", "/api/documents/**").permitAll()`
- **Ảnh hưởng:**
  - Bất kỳ ai đọc được danh sách sinh viên (email, số điện thoại, địa chỉ, ngày sinh).
  - Tải được tài liệu qua `/api/documents/download/{id}`.
  - `/api/documents/download?filePath=...` cho phép truyền **đường dẫn object tùy ý trong bucket**, không kiểm tra tài liệu đó có tồn tại trong DB hay thuộc về ai.
- **Hướng khắc phục:** Chỉ cho phép GET công khai với courses/departments; students/documents yêu cầu xác thực; bỏ hoặc hạn chế endpoint download theo `filePath`; kiểm tra quyền sở hữu.

### A4. Phân quyền gần như không hoạt động

- **Vị trí:** `config/SecurityConfig.java:94-107`, `rest/SecurityRest.java:30,45`
- **Nguyên nhân:**
  - `anyRequest().authenticated()` cho toàn bộ POST/PUT/DELETE → user role `USER` vẫn tạo/sửa/xóa được courses, students, departments, documents.
  - `@PreAuthorize` chỉ đặt ở 2 endpoint `/api/security/**` và dùng `hasRole('LECTURER')` — trong khi hệ thống chỉ có `ADMIN`, `TEACHER`, `USER` (`UserDetailsServiceImpl` tiền tố `ROLE_`).
- **Ảnh hưởng:** TEACHER bị 403 ở `/api/security/**`; các API ghi không phân biệt vai trò.
- **Hướng khắc phục:** Map đúng role (`TEACHER`/`LECTURER` thống nhất), thêm `@PreAuthorize` cho API ghi và phân quyền theo tài nguyên.

### A5. Secret và tài khoản mặc định hardcode

- **Vị trí:**
  - `application.properties:39` — `jwt.secret` có giá trị mặc định
  - `security/jwt/JwtTokenProvider.java:23` — fallback secret trong `@Value`
  - `service/impl/SecurityServiceImpl.java:25` — AES key hardcode
  - `common/converter/AesEncryptConverter.java:23` — AES key hardcode (trùng)
  - `config/DataInitializer.java:56-58,117` — tạo `admin/123456`, `gv_nam/123456`, `student_a/123456` mỗi lần khởi động
- **Ảnh hưởng:** Ai đọc source là ký được JWT hợp lệ/giải mã dữ liệu; tài khoản admin mặc định yếu.
- **Hướng khắc phục:** Bắt buộc lấy từ biến môi trường, không có fallback; đổi mật khẩu seed; cân nhắc tắt seed ở production.

### A6. Upload MinIO không đồng bộ với transaction DB

- **Vị trí:** `service/impl/DocumentServiceImpl.java:59-96`, `service/MinioStorageService.java:42-58`
- **Nguyên nhân:** Upload object lên MinIO trước, sau đó mới ghi DB trong transaction; lỗi ở file thứ N hoặc rollback DB không xóa các object đã upload.
- **Ảnh hưởng:** Object rác trong MinIO, sai lệch dữ liệu; `InputStream` của MultipartFile không được đóng.
- **Hướng khắc phục:** Upload theo cơ chế "tất cả hoặc không" (rollback thủ công khi lỗi) hoặc lưu DB trước rồi upload, có job dọn rác; dùng try-with-resources.

---

## 4. 🟠 LỖI CHỨC NĂNG ĐÃ XÁC NHẬN

### B1. Tìm kiếm sinh viên trên Web UI luôn lỗi 400

- **Vị trí:** `src/main/resources/static/index.html:486` vs `rest/StudentRest.java:57`
- **Chi tiết:** UI gọi `/api/students/search?name=...`, backend yêu cầu `@RequestParam String keyword` → thiếu tham số bắt buộc.
- **Khắc phục:** Đổi UI thành `?keyword=...`.

### B2. Lọc tài liệu theo appId trên UI không hoạt động

- **Vị trí:** `index.html:559` vs `rest/DocumentRest.java:45-46`
- **Chi tiết:** UI gọi `/api/documents/list?appId=...` nhưng `getAllActiveDocuments()` bỏ qua `appId`, trả toàn bộ tài liệu.
- **Khắc phục:** Dùng `/api/documents/app/{appId}` hoặc bổ sung `appId` vào endpoint list.

### B3. Postman sai tên tham số

- **Vị trí:**
  - `docs/Course Management System - Full APIs.postman_collection.json:226` → `/api/courses/by-title?title=...`
  - `...:741` → `/api/students/by-email?email=...`
  - API thực tế: `CourseRest.java:29-32` (`queryTitle`), `StudentRest.java:29-32` (`queryEmail`)
- **Ảnh hưởng:** Request luôn trả 404 vì cả `title`/`email` đều null.
- **Khắc phục:** Đổi Postman sang `queryTitle`/`queryEmail`, hoặc đổi API cho khớp tài liệu.

### B4. `/api/auth/me` không token trả 404 thay vì 401

- **Vị trí:** `AuthRestImpl.java:116-123`, `SecurityConfig.java:100`
- **Chi tiết:** `/api/auth/**` được `permitAll`, Spring inject `AnonymousAuthenticationToken`; token này `isAuthenticated()=true`, nên code đi tiếp và tìm user `anonymousUser` → 404.
- **Khắc phục:** Kiểm tra `authentication instanceof AnonymousAuthenticationToken` hoặc trả 401.

### B5. Check trùng mã khoa trước khi chuẩn hóa

- **Vị trí:** `service/impl/DepartmentServiceImpl.java:33` (create), `:55` (update)
- **Chi tiết:** So sánh `dto.getDepartmentCode()` gốc, sau đó mới `trim().toUpperCase()`. Nhập `"cntt"` sẽ không phát hiện trùng `"CNTT"` → insert → vi phạm unique → 409.
- **Khắc phục:** Chuẩn hóa trước khi kiểm tra.

### B6. `departmentId` không tồn tại bị bỏ qua im lặng

- **Vị trí:** `service/impl/StudentServiceImpl.java:219-223`
- **Chi tiết:** Nếu `departmentDao.getById()` trả null thì không set (tạo mới → department null; cập nhật → giữ khoa cũ). Cũng không thể xóa khoa của sinh viên vì null bị bỏ qua.
- **Khắc phục:** Ném `BadRequestException` khi department không tồn tại; hỗ trợ explicit clear.

### B7. Batch create không validate từng phần tử

- **Vị trí:** `rest/CourseRest.java:34-35`, `rest/StudentRest.java:34-35`, `StudentServiceImpl.java:138-151`
- **Chi tiết:** `List<CourseRequestDTO>` không có `@Valid` trên phần tử; batch student không kiểm tra trùng email → lỗi constraint DB, trả 409/500 chung chung.
- **Khắc phục:** Dùng `List<@Valid DTO>` + kiểm tra nghiệp vụ từng phần tử, trả danh sách lỗi.

### B8. Tài liệu đã xóa mềm vẫn xuất hiện ở một số endpoint

- **Vị trí:** `dao/impl/DocumentDaoImpl.java:161-164` (kế thừa `findAllPaged`, `searchBySpecificationPaged`)
- **Chi tiết:** `/paged`, `/sorted`, `/spec-search-paged` không lọc `deleted = false`, khác với `/list` và `/app/{appId}`.
- **Khắc phục:** Áp dụng điều kiện `deleted=false` nhất quán.

### B9. Xóa khoa đang có sinh viên trả thông báo sai nội dung

- **Vị trí:** `common/exception/GlobalExceptionHandler.java:80-90`
- **Chi tiết:** Mọi `DataIntegrityViolationException` đều trả "ví dụ: email đã tồn tại", kể cả khi lỗi là FK từ bảng students → department.
- **Khắc phục:** Phân loại constraint hoặc trả thông báo trung tính + kiểm tra ràng buộc trước khi xóa.

---

## 5. 🟡 LỖI TRUNG BÌNH - BẢO MẬT & KIẾN TRÚC

### C1. REST gọi thẳng DAO (vi phạm Strict 3-Layer)

- **Vị trí:** `rest/impl/AuthRestImpl.java:30,55,74,94,122`
- **Chi tiết:** Inject `IUserDao`, chứa logic đăng ký/đăng nhập trong controller, bỏ qua tầng Service.
- **Khắc phục:** Tạo `AuthService`/`AuthServiceImpl`, controller chỉ gọi service.

### C2. CORS cấu hình xung đột

- **Vị trí:** `config/SecurityConfig.java:68-80` (`allowCredentials(true)`), các controller `@CrossOrigin(origins="*")` (`CourseRestImpl:23`, `StudentRestImpl:23`, `DocumentRestImpl:22`, `SecurityRestImpl:21`)
- **Kiểm chứng:** Đã chạy thử trực tiếp `CorsConfiguration` của Spring 7.0.9: `checkOrigin()` ném `IllegalArgumentException` khi `allowCredentials=true` và `allowedOrigins` chứa `"*"`.
- **Ảnh hưởng:** Request cross-origin thật (frontend khác origin) nhận HTTP 500 thay vì header CORS.
- **Khắc phục:** Bỏ `@CrossOrigin` (đã có cấu hình global) hoặc đổi sang `allowedOriginPatterns`.

### C3. GlobalExceptionHandler lộ thông tin nội bộ và thiếu handler

- **Vị trí:** `GlobalExceptionHandler.java:132-142` và toàn bộ class
- **Chi tiết:**
  - Handler 500 trả `ex.getMessage()` ra client → có thể lộ SQL, tên bảng, stack.
  - Thiếu handler cho: `MissingServletRequestParameterException`, `MaxUploadSizeExceededException`, `ConstraintViolationException`, `HttpRequestMethodNotSupportedException`, `NoResourceFoundException`.
- **Khắc phục:** Luôn trả `MessageConstants.INTERNAL_SERVER_ERROR` (đã có sẵn), bổ sung các handler còn thiếu.

### C4. `AesEncryptConverter` là dead code

- **Vị trí:** `common/converter/AesEncryptConverter.java:15-16`
- **Chi tiết:** Không entity/field nào dùng `@Convert`, nên converter chưa từng được áp dụng. Ngoài ra:
  - AES-CBC không có MAC/integrity.
  - Lỗi giải mã trả nguyên ciphertext (che lỗi).
  - Key hardcode trùng với `SecurityServiceImpl`.
- **Khắc phục:** Hoặc áp dụng thực tế cho các field nhạy cảm, hoặc loại bỏ; chuyển sang AES-GCM và key từ env.

### C5. Trả Entity thay vì DTO

- **Vị trí:** `CourseRest.java:15,18`, `StudentRest.java:15,18`
- **Chi tiết:** `POST/PUT /api/courses`, `/api/students` trả `ResponseEntity<Course>` / `ResponseEntity<Student>`, không nhất quán với các endpoint trả DTO.
- **Khắc phục:** Trả `CourseResponseDTO` / `StudentResponseDTO`.

### C6. Thông báo hardcode thay vì `MessageConstants`

- **Vị trí:**
  - `CourseServiceImpl.java:101,111`
  - `StudentServiceImpl.java:39,57,107,117`
  - `DocumentServiceImpl.java:51,54,65,71,94,146,221,287`
  - `DepartmentServiceImpl.java:34,52,57,74,84,94`
- **Chi tiết:** Vi phạm quy tắc 8 của chuẩn dự án (tập trung message tại `common`).
- **Khắc phục:** Bổ sung constant và thay thế.

### C7. Sort/Page không kiểm soát

- **Vị trí:** `HibernatePaginationSortingDao.java:174-181`, các `@RequestParam int size`
- **Chi tiết:** `sortBy` không kiểm tra property tồn tại → `PropertyReferenceException` (500); `size` không giới hạn → client xin page rất lớn gây tốn bộ nhớ.
- **Khắc phục:** Validate sort field theo metadata entity; `@Min/@Max` cho `page`, `size`.

### C8. `GenericSpecification` xử lý kiểu dữ liệu sai

- **Vị trí:** `specification/GenericSpecification.java:40-99`
- **Chi tiết:**
  - Field `Date/LocalDate` rơi vào nhánh `Comparable` không phải `Number` → so sánh với String → 500.
  - `!` = NOT LIKE (chứa chuỗi con), `!=` = not equal → ngữ nghĩa khác nhau dù tên gần giống.
  - Field không tồn tại bị bỏ qua im lặng, search có thể trả về toàn bộ dữ liệu.
- **Khắc phục:** Parse theo `javaType` (Date, LocalDate, Enum...); thống nhất ngữ nghĩa toán tử; trả lỗi khi field không hợp lệ.

---

## 6. 🟡 LỖI TRUNG BÌNH - VẬN HÀNH / DOCKER / TÀI LIỆU

### D1. Chatbot trong Docker không truy cập được từ host

- **Vị trí:** `chatbot/web_app.py:1534`, `docker-compose.yml:86`
- **Chi tiết:** `app.run(host="127.0.0.1")` chỉ lắng nghe loopback trong container; publish `7860:7860` không hoạt động.
- **Khắc phục:** Bind `0.0.0.0` (có thể đọc host từ env).

### D2. Hardcode đường dẫn Windows trong chatbot

- **Vị trí:** `chatbot/web_app.py:10` (`HF_HOME = D:\.cache\huggingface`), `:39` (`D:\models\Qwen2.5-Coder-3B-Instruct-sharded`)
- **Ảnh hưởng:** Hỏng khi chạy Linux/container; trên Linux tạo thư mục tên `D:\.cache...`.
- **Khắc phục:** Dùng env var có fallback tương đối.

### D3. Thiếu `bitsandbytes` khi chạy GPU 4-bit

- **Vị trí:** `chatbot/requirements.txt:1-6`, `chatbot/web_app.py:85-95`
- **Chi tiết:** Code dùng `BitsAndBytesConfig(load_in_4bit=True)` khi có CUDA, nhưng requirements không có `bitsandbytes`; README cũng không cài.
- **Ảnh hưởng:** Chạy theo hướng dẫn trên máy có GPU → ImportError hoặc không quantize được.
- **Khắc phục:** Thêm `bitsandbytes` (kèm lưu ý nền tảng), hoặc tự động fallback CPU khi thiếu.

### D4. `start_all.bat` hardcode JDK

- **Vị trí:** `start_all.bat` — `C:\Users\Admin\.jdks\openjdk-26.0.2.1`
- **Ảnh hưởng:** Không chạy được trên máy khác; JDK 26 không phải JDK 21 khai báo trong pom.
- **Khắc phục:** Dùng `JAVA_HOME` hiện có hoặc kiểm tra `java -version`.

### D5. Cấu hình production chưa an toàn

- **Vị trí:** `src/main/resources/application.properties:17-21,39`
- **Chi tiết:** `ddl-auto=update`, `show-sql=true`, `open-in-view=true`, credential/secret mặc định.
- **Khắc phục:** Dùng profile `dev/prod`, migration (Flyway/Liquibase), tắt show-sql, bắt buộc env.

### D6. Tài liệu API lệch với code

- **Vị trí:** `docs/openapi.json` (dùng `/api/v1/*`), `README.md`
- **Chi tiết:** Code thực tế `/api/*`; README mô tả 2 controller nhưng có 6; `swagger-annotations 1.6.14` (Swagger 2) bị springdoc (OpenAPI 3) bỏ qua nên mô tả `SecurityRest` không hiển thị.
- **Khắc phục:** Đồng bộ openapi/README; chuyển sang annotation `io.swagger.v3.oas.annotations`.

### D7. Chatbot phụ thuộc model local

- **Vị trí:** `chatbot/web_app.py:38-40`
- **Chi tiết:** Mặc định tải `Qwen/Qwen2.5-Coder-3B-Instruct` từ HuggingFace nếu không có thư mục local; trong container không có internet/không mount model sẽ khởi động chậm hoặc lỗi.
- **Khắc phục:** Mount model hoặc cấu hình đường dẫn qua env, có health check rõ ràng.

---

## 7. 🔵 LỖI THẤP / VỆ SINH CODE

| # | Vị trí | Chi tiết |
|---|---|---|
| E1 | `CourseDaoImpl.java:7-8,13`, `StudentDaoImpl.java:7-8,13`, `DepartmentDaoImpl.java:7-8` | Import thừa (`NoResultException`, `TypedQuery`, `Collections`). |
| E2 | `entity/Document.java:6,34,68-71` | Dùng `java.util.Date` không đồng nhất; `@GeneratedValue(strategy = UUID)` + gán UUID thủ công trong `@PrePersist` là dư thừa. |
| E3 | `security/jwt/JwtAuthenticationEntryPoint.java:34`, `JwtAccessDeniedHandler.java:34` | Dùng `request.getServletPath()` có thể rỗng; nên dùng `getRequestURI()`. |
| E4 | `service/impl/DocumentServiceImpl.java:153-156` | `Content-Disposition` chưa theo RFC 5987 (filename*), tên file tiếng Việt có thể sai trên một số trình duyệt. |
| E5 | `security/jwt/JwtAuthenticationFilter.java:47-49` | Nuốt toàn bộ exception (kể cả DB down) → request thành unauthenticated âm thầm, khó debug. |
| E6 | `MinioStorageService.java:43` | `ensureBucketExists()` gọi lại mỗi lần upload (1 round-trip thừa); nên kiểm tra một lần khi khởi động. |
| E7 | `DepartmentRestImpl.java` | Không có try/catch + logging theo chuẩn REST của dự án (các controller khác đều có). |

---

## 8. ĐIỂM ĐANG HOẠT ĐỘNG TỐT

- Build và 45 unit test đều pass, Spring context khởi động thành công.
- Cây Generic DAO `IGenericDao → IPaginationSortingDao → IEntityDao` đúng thiết kế; CRUD/phân trang/sort cơ bản hoạt động.
- JWT filter/provider, BCrypt, thống nhất format lỗi `ErrorResponse`, MinIO tự tạo bucket đúng hướng.
- Soft-delete và versioning tài liệu đúng logic chính (thiếu rollback MinIO và lọc `deleted` ở một số endpoint).
- UI tĩnh và Postman khá đầy đủ, chỉ lệch một số tên tham số.

---

## 9. THỨ TỰ ƯU TIÊN SỬA ĐỀ XUẤT

1. **A1** – Sửa alias JPQL `getDoc` (ảnh hưởng trực tiếp API tài liệu).
2. **A2** – Chặn client tự gán role khi đăng ký.
3. **A3 + A4** – Siết quyền GET dữ liệu nhạy cảm, bỏ download theo `filePath`, thêm phân quyền cho API ghi, sửa role `LECTURER/TEACHER`.
4. **A5** – Loại bỏ secret/tài khoản mặc định hardcode.
5. **B1, B2, B3** – Sửa UI và Postman (nhanh, ảnh hưởng trải nghiệm).
6. **A6 + B7 + B8** – Đồng bộ transaction MinIO, validate batch, lọc `deleted`.
7. **C2, C3, C4** – CORS, exception handler, xử lý converter AES.
8. **D1-D7** – Docker, đường dẫn, tài liệu, cấu hình production.

---

## 10. GHI CHÚ

- Báo cáo này **chưa thay đổi mã nguồn**. Theo quy định dự án, trước khi sửa cần:
  1. Liệt kê file/dòng cụ thể sẽ thay đổi.
  2. Backup bằng Git (`git commit`/`git branch`/`git tag`).
  3. Chờ người dùng xác nhận.
- Các đường dẫn dòng có thể lệch nếu file được sửa sau thời điểm rà soát.
