# Kiến trúc 3 tầng & Nguyên tắc cách ly (3-Layer Architecture Standards)

Tài liệu này quy định chi tiết về cấu trúc phân tầng, phân tách interface - implementation, các quy ước đặt tên và các điều cấm kỵ (anti-patterns) trong dự án Course Management System.

---

## 1. Cấu trúc Package chuẩn

```text
com.mkii.coursemanagementsystem/
├── common/                     # Hằng số, Exception, Response format
│   ├── ApiConstants.java
│   ├── MessageConstants.java
│   └── exception/
│       ├── BadRequestException.java
│       ├── ResourceNotFoundException.java
│       ├── GlobalExceptionHandler.java
│       └── ErrorResponse.java
├── config/                     # Cấu hình Spring (MinIO, Web, Security,...)
│   └── MinioConfig.java
├── entity/                     # Các JPA Entities & Named Queries
│   ├── Course.java
│   ├── Student.java
│   └── Document.java
├── dao/                        # Interface tầng truy cập dữ liệu
│   ├── IGenericDao.java
│   ├── IPaginationSortingDao.java
│   ├── ICourseDao.java
│   ├── IStudentDao.java
│   ├── IDocumentDao.java
│   └── impl/                   # Triển khai tầng DAO
│       ├── CourseDaoImpl.java
│       ├── StudentDaoImpl.java
│       └── DocumentDaoImpl.java
├── hibernateDao/               # Generic base classes độc lập
│   ├── HibernateGenericDao.java
│   └── HibernatePaginationSortingDao.java
├── service/                    # Interface tầng nghiệp vụ
│   ├── CourseService.java
│   ├── StudentService.java
│   ├── DocumentService.java
│   ├── MinioStorageService.java
│   └── impl/                   # Triển khai tầng nghiệp vụ
│       ├── CourseServiceImpl.java
│       ├── StudentServiceImpl.java
│       ├── DocumentServiceImpl.java
│       └── MinioStorageServiceImpl.java
├── rest/                       # Interface tầng API Controllers
│   ├── CourseRest.java
│   ├── StudentRest.java
│   ├── DocumentRest.java
│   └── impl/                   # Triển khai tầng API Controllers
│       ├── CourseRestImpl.java
│       ├── StudentRestImpl.java
│       └── DocumentRestImpl.java
└── specification/              # JPA Dynamic Specification Query Engine
    ├── SearchCriteria.java
    ├── GenericSpecification.java
    └── GenericSpecificationsBuilder.java
```

---

## 2. Nguyên tắc cách ly nghiêm ngặt (Strict Layer Isolation)

### Quy tắc 1: Service chỉ được phép tương tác với DAO thông qua Interface
* **ĐÚNG:**
  ```java
  @Service
  public class DocumentServiceImpl implements DocumentService {
      private final IDocumentDao documentDao; // <-- CHỈ INJECT INTERFACE
      private final MinioStorageService minioStorageService;

      public DocumentServiceImpl(IDocumentDao documentDao, MinioStorageService minioStorageService) {
          this.documentDao = documentDao;
          this.minioStorageService = minioStorageService;
      }
      ...
  }
  ```
* **SAI (Nghiêm cấm):**
  ```java
  // KHÔNG ĐƯỢC inject class triển khai:
  @Autowired private DocumentDaoImpl documentDaoImpl; 

  // KHÔNG ĐƯỢC inject trực tiếp EntityManager vào Service:
  @Autowired private EntityManager entityManager; 

  // KHÔNG ĐƯỢC inject trực tiếp Hibernate base DAO:
  @Autowired private HibernateGenericDao<String, Document> genericDao; 
  ```

### Quy tắc 2: Tầng REST Controller luôn có Interface định nghĩa hợp đồng API
* Mọi Controller phải có một Interface tương ứng đặt ở package `rest`.
* Interface định nghĩa: đường dẫn endpoint (`@GetMapping`, `@PostMapping`,...), tham số (`@RequestParam`, `@PathVariable`, `@RequestBody`), và kiểu trả về `ResponseEntity<?>`.
* Class triển khai (`rest.impl.*`) implement interface, gắn `@RestController`, `@RequestMapping(...)`, `@CrossOrigin(origins = "*")`.
* Từng method trong Controller phải:
  1. Ghi log đầu vào bằng `logger.info(...)`.
  2. Bọc toàn bộ xử lý trong khối `try { ... } catch (Exception e) { ... }`.
  3. Ghi log lỗi bằng `logger.error(...)`.
  4. Trả về `ResponseEntity.status(...).body(...)`.

### Quy tắc 3: Tầng `hibernateDao` chỉ chứa các Generic Abstract/Base Classes
* Thư mục `hibernateDao` tuyệt đối không chứa các DAO cụ thể của từng Entity (`CourseDaoImpl`, `DocumentDaoImpl`).
* Toàn bộ DAO triển khai cụ thể phải nằm trong `dao.impl`.
* `hibernateDao` đóng vai trò là một framework nội bộ độc lập cung cấp CRUD, JPQL Helpers, Pagination, Sorting và Specification integration.

---

## 3. Các điều cấm kỵ (Anti-Patterns to Avoid)

1. **Bỏ qua tầng Service**: REST Controller gọi thẳng vào DAO. (Mọi logic phải đi qua Service).
2. **Hardcode chuỗi thông báo lỗi**: Phải sử dụng hằng số từ `MessageConstants` hoặc `ApiConstants`.
3. **Hardcode chuỗi SQL/JPQL động mà không kiểm tra tên cột**: Khi ghép tên cột vào JPQL, bắt buộc gọi hàm `isValidIdentifier(fieldName)` để ngăn ngừa triệt để SQL/JPQL Injection.
4. **Trả về Entity trực tiếp mà không kiểm soát JSON Serialization**: Cần chú ý lazy loading, vòng lặp tham chiếu hai chiều hoặc các trường nhạy cảm.

---

## 4. Chuẩn hóa Bảo mật Phân quyền (RBAC) & Tài liệu Swagger / OpenAPI

### 1. Phân quyền theo vai trò (Role-Based Access Control với `@PreAuthorize`)
* Bật cấu hình bảo mật phương thức: `@EnableMethodSecurity(prePostEnabled = true)`.
* Các vai trò trong hệ thống:
  * `ROLE_ADMIN`: Toàn quyền hệ thống (Tạo, cập nhật, xóa, cấu hình).
  * `ROLE_LECTURER`: Giảng viên (Tạo/cập nhật khóa học, quản lý tài liệu, xem thông tin sinh viên).
  * `ROLE_STUDENT`: Sinh viên (Xem thông tin khóa học, xem danh sách sinh viên, tải/đọc tài liệu).
* Nguyên tắc gán `@PreAuthorize` trực tiếp tại REST Interface:
  * Thao tác phá hủy (Xóa dữ liệu, batch create): `@PreAuthorize("hasRole('ADMIN')")`.
  * Thao tác tạo/cập nhật nghiệp vụ: `@PreAuthorize("hasRole('ADMIN') or hasRole('LECTURER')")`.
  * Thao tác đọc/tra cứu: `@PreAuthorize("hasRole('STUDENT') or hasRole('LECTURER') or hasRole('ADMIN')")`.

### 2. Chuẩn hóa Swagger / OpenAPI Annotations
* Interface REST được gắn:
  * `@Api(tags = {"{Entity}Rest"})`
  * `@SwaggerDefinition(tags = {@Tag(name = "...", description = "...")})`
* Từng endpoint được mô tả chi tiết:
  * `@ApiOperation(value = "...", tags = {...}, authorizations = {@Authorization(...)})`
  * `@ApiResponses(value = {@ApiResponse(code = 200, message = "..."), ...})`
  * `@ApiParam(value = "...", required = true/false)` trên từng tham số.

### 3. Tối ưu hóa CORS Preflight Caching
* Controller gắn annotation: `@CrossOrigin(origins = "*", maxAge = 3600)` để trình duyệt lưu cache kết quả kiểm tra CORS preflight trong 1 giờ.
