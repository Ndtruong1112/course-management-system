# 01. Phân tầng kiến trúc & Quy chuẩn Package Layout

Tài liệu này cung cấp các tiêu chuẩn chi tiết về việc phân vùng trách nhiệm (Separation of Concerns), phân tách Interface - Implementation, Dependency Injection, và cách ly tuyệt đối giữa DTO và JPA Entity trong các ứng dụng Spring Boot.

---

## 1. Nguyên tắc phân chia trách nhiệm giữa các tầng (Layer Responsibilities)

| Tầng (Layer) | Trách nhiệm chính (DO) | Những điều cấm kỵ (DON'T) |
| :--- | :--- | :--- |
| **Controller / REST** | - Nhận HTTP Request, trích xuất Header, Path, Query, Body.<br>- Kích hoạt Bean Validation (`@Valid`).<br>- Gọi tầng Service.<br>- Đóng gói dữ liệu vào `ResponseEntity<ApiResponse<T>>`. | - **CẤM** chứa logic nghiệp vụ tính toán.<br>- **CẤM** gọi trực tiếp Repository.<br>- **CẤM** nhận hoặc trả về JPA Entity.<br>- **CẤM** tự viết câu lệnh SQL/HQL. |
| **Service** | - Chứa toàn bộ Business Logic, quy tắc tính toán, kiểm tra nghiệp vụ.<br>- Điều phối các Repository, Service khác, External APIs.<br>- Quản lý ranh giới giao dịch (`@Transactional`).<br>- Áp dụng các Technical Helper Utilities (Mã hóa, xử lý file, parse chuỗi).<br>- Ném ra các Business Exceptions với message chuẩn. | - **CẤM** phụ thuộc vào `HttpServletRequest`, `HttpServletResponse`, hoặc các đối tượng HTTP.<br>- **CẤM** trả về mã HTTP status code (như `HttpStatus.OK`). |
| **Repository / DAO** | - Thao tác trực tiếp với cơ sở dữ liệu qua Spring Data JPA / Hibernate.<br>- Định nghĩa các phương thức tìm kiếm, sắp xếp, phân trang.<br>- Thực thi các câu query tối ưu (Criteria, Specification, `@Query`). | - **CẤM** chứa logic nghiệp vụ.<br>- **CẤM** ném ra các ngoại lệ nghiệp vụ người dùng (như "Số dư không đủ"). |
| **DTO (Request / Response)** | - Đại diện cho cấu trúc dữ liệu trao đổi qua API.<br>- Khai báo các ràng buộc validation trên Request (`@NotBlank`, `@Min`, `@Max`).<br>- Chỉ phơi bày các thuộc tính an toàn, che giấu dữ liệu nhạy cảm. | - **CẤM** gắn annotation JPA (`@Entity`, `@Table`, `@Id`).<br>- **CẤM** chứa logic truy vấn DB. |
| **Entity** | - Đại diện cho bảng trong Database (Object-Relational Mapping).<br>- Định nghĩa khóa chính, các cột, quan hệ (`@ManyToOne`, `@OneToMany`), chỉ mục (`@Index`). | - **CẤM** gửi trực tiếp về phía Client.<br>- **CẤM** dùng làm tham số `@RequestBody` ở Controller. |

---

## 2. Quy chuẩn Interface - Implementation

### Tại sao bắt buộc dùng Interface cho Tầng Service?
1. **Loose Coupling (Giảm sự phụ thuộc chặt chẽ):** Controller chỉ phụ thuộc vào hợp đồng (Contract) mà Service cam kết, không phụ thuộc vào chi tiết triển khai bên dưới.
2. **Dễ dàng Mocking trong Unit Test:** Cho phép tạo Mock Object của Interface dễ dàng mà không cần khởi tạo các thành phần nặng của Class thực thi.
3. **Hỗ trợ Spring AOP & Proxies:** Đảm bảo các cơ chế Proxy của Spring hoạt động tối ưu nhất (Dynamic Proxy của JDK).
4. **Khả năng mở rộng:** Cho phép có nhiều class triển khai khác nhau (ví dụ: `PaymentServiceImplV1`, `PaymentServiceImplV2`, `FakePaymentServiceImpl` cho môi trường Test).

### Cấu trúc thư mục & Naming Convention:
```text
service/
├── UserService.java            # Interface: public interface UserService { ... }
└── impl/
    └── UserServiceImpl.java    # Implementation: @Service public class UserServiceImpl implements UserService { ... }
```

---

## 3. Tiêu chuẩn Dependency Injection: Constructor Injection

### Quy tắc bất biến:
- **TUYỆT ĐỐI CẤM:** Field Injection dùng `@Autowired` trực tiếp lên field:
  ```java
  // ANTI-PATTERN: KHÔNG BAO GIỜ DÙNG
  @Service
  public class UserServiceImpl implements UserService {
      @Autowired
      private UserRepository userRepository; // Rủi ro: Khó test, vi phạm tính bất biến, dễ dính NullPointerException
  }
  ```

- **BẮT BUỘC DÙNG:** Constructor Injection kết hợp `private final`:
  ```java
  // STANDARD PATTERN: Khuyên dùng kết hợp Lombok @RequiredArgsConstructor
  @Service
  @RequiredArgsConstructor
  public class UserServiceImpl implements UserService {

      private final UserRepository userRepository;
      private final UserMapper userMapper;
      private final SecurityService securityService;
  }
  ```
  *Lợi ích:*
  - Các dependency được bảo đảm khởi tạo đầy đủ khi đối tượng được tạo (`final`).
  - Dễ dàng viết Unit Test thủ công bằng `new UserServiceImpl(mockRepo, mockMapper, mockSecurity)`.
  - Giúp phát hiện sớm "God Class" (nếu class có quá nhiều tham số trong constructor, cần tách nhỏ Service).

---

## 4. Chuyển đổi DTO ⬌ Entity (Mapping Strategy)

### Quy tắc cách ly:
Mọi dữ liệu đi vào hệ thống qua Request DTO phải được map sang Entity trước khi lưu vào Database. Mọi dữ liệu lấy từ Entity phải được map sang Response DTO trước khi trả về Controller.

### Khuyến nghị công cụ:
1. **MapStruct (Khuyên dùng cho hiệu năng cao & an toàn kiểu):**
   ```java
   @Mapper(componentModel = "spring")
   public interface UserMapper {
       UserResponse toResponse(User entity);
       User toEntity(CreateUserRequest request);
       void updateEntityFromDto(UpdateUserRequest dto, @MappingTarget User entity);
   }
   ```
2. **Manual Mapping (Phù hợp logic chuyển đổi phức tạp hoặc dự án nhỏ):**
   ```java
   public final class UserConverter {
       public static UserResponse toResponse(User entity) {
           if (entity == null) return null;
           return UserResponse.builder()
                   .id(entity.getId())
                   .username(entity.getUsername())
                   .email(entity.getEmail())
                   .fullName(entity.getFullName())
                   .createdAt(entity.getCreatedAt())
                   .build();
       }
   }
   ```
