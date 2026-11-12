# 02. Chuẩn mực Thiết kế REST API & Response Wrapper

Tài liệu này định nghĩa các nguyên tắc chuẩn mực cho việc thiết kế endpoint RESTful, quy chuẩn mã trạng thái HTTP (Status Codes), cấu trúc phản hồi hợp nhất (`ApiResponse<T>`), phân trang (`PageResponse<T>`), và Bean Validation.

---

## 1. Quy chuẩn đặt tên URI (RESTful URL Conventions)

1. **Sử dụng danh từ số nhiều (Plural Nouns):**
   - ĐÚNG: `/api/v1/users`, `/api/v1/courses`, `/api/v1/orders`
   - SAI: `/api/v1/user`, `/api/v1/getUser`, `/api/v1/createOrder`
2. **Ký tự chữ thường, phân cách bằng dấu gạch ngang (kebab-case):**
   - ĐÚNG: `/api/v1/course-registrations`, `/api/v1/payment-transactions`
   - SAI: `/api/v1/courseRegistrations`, `/api/v1/payment_transactions`
3. **Mối quan hệ phân cấp lồng nhau (Nesting Resources) tối đa 2 cấp:**
   - ĐÚNG: `/api/v1/courses/{courseId}/students` (Lấy danh sách sinh viên của khóa học)
   - ĐÚNG: `/api/v1/students/{studentId}/documents` (Lấy tài liệu của sinh viên)
   - SAI: `/api/v1/faculties/{facultyId}/departments/{departmentId}/courses/{courseId}/students` (Quá sâu, nên tách thành `/api/v1/courses/{id}/students`)
4. **Không đưa hành động vào URI (Dùng HTTP Methods):**
   - Lấy danh sách: `GET /api/v1/courses`
   - Lấy chi tiết: `GET /api/v1/courses/{id}`
   - Tạo mới: `POST /api/v1/courses`
   - Cập nhật toàn bộ: `PUT /api/v1/courses/{id}`
   - Cập nhật một phần: `PATCH /api/v1/courses/{id}`
   - Xóa: `DELETE /api/v1/courses/{id}`
   - Tìm kiếm lọc động: `GET /api/v1/courses?search=status:ACTIVE,title:Java&page=0&size=10&sort=createdAt,desc`

---

## 2. Bảng mã trạng thái HTTP chuẩn (HTTP Status Codes)

| Mã HTTP | Tên chuẩn | Khi nào sử dụng? |
| :---: | :--- | :--- |
| **200** | `OK` | Truy vấn thành công (`GET`), hoặc cập nhật thành công (`PUT`, `PATCH`). |
| **201** | `CREATED` | Tạo mới tài nguyên thành công (`POST`). Có thể trả về kèm header `Location`. |
| **204** | `NO CONTENT` | Thao tác thành công nhưng không cần trả body (thường dùng cho `DELETE`). |
| **400** | `BAD REQUEST` | Dữ liệu gửi lên sai định dạng, thiếu trường bắt buộc, hoặc vi phạm validation logic. |
| **401** | `UNAUTHORIZED` | Yêu cầu cần xác thực danh tính (chưa đăng nhập, thiếu JWT token, hoặc token hết hạn). |
| **403** | `FORBIDDEN` | Đã đăng nhập nhưng không đủ quyền hạn/vai trò (Role-based access denied). |
| **404** | `NOT FOUND` | Tài nguyên không tồn tại trong hệ thống (ID không có trong DB, URI sai). |
| **409** | `CONFLICT` | Xung đột dữ liệu (Email/Username đã tồn tại, trùng lặp phiên bản, Optimistic Lock). |
| **422** | `UNPROCESSABLE ENTITY` | Cú pháp JSON đúng nhưng vi phạm quy tắc nghiệp vụ logic cụ thể. |
| **500** | `INTERNAL SERVER ERROR` | Lỗi ngoài ý muốn từ phía server (Ngoại lệ chưa bắt, lỗi DB sập). |

---

## 3. Cấu trúc phản hồi API chuẩn (Unified API Response Wrapper)

Mọi API trả về cho Frontend hoặc Mobile App **phải tuân theo định dạng JSON đồng nhất**:

### Class triển khai mẫu: `ApiResponse<T>`

```java
package com.company.project.common;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {

    @Builder.Default
    private boolean success = true;

    private String message;

    private T data;

    @Builder.Default
    private LocalDateTime timestamp = LocalDateTime.now();

    public static <T> ApiResponse<T> ok(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .message("Thao tác thành công")
                .data(data)
                .build();
    }

    public static <T> ApiResponse<T> ok(String message, T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .message(message)
                .data(data)
                .build();
    }

    public static <T> ApiResponse<T> created(String message, T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .message(message)
                .data(data)
                .build();
    }
}
```

---

## 4. Cấu trúc phản hồi phân trang chuẩn (`PageResponse<T>`)

Để Client hiển thị thanh chuyển trang chính xác, luôn bọc dữ liệu phân trang trong `PageResponse<T>`:

```java
package com.company.project.common;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.domain.Page;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PageResponse<T> {

    private List<T> content;
    private int pageNumber;
    private int pageSize;
    private long totalElements;
    private int totalPages;
    private boolean isFirst;
    private boolean isLast;

    public static <T> PageResponse<T> from(Page<T> page) {
        return PageResponse.<T>builder()
                .content(page.getContent())
                .pageNumber(page.getNumber())
                .pageSize(page.getSize())
                .totalElements(page.getTotalElements())
                .totalPages(page.getTotalPages())
                .isFirst(page.isFirst())
                .isLast(page.isLast())
                .build();
    }
}
```

---

## 5. Quy chuẩn Bean Validation tại tầng Controller

Sử dụng `@Valid` kết hợp Jakarta Bean Validation trên các Request DTO:

```java
@Data
public class CreateStudentRequest {

    @NotBlank(message = "{student.name.not_blank}")
    @Size(min = 2, max = 50, message = "{student.name.size}")
    private String fullName;

    @NotBlank(message = "{student.email.not_blank}")
    @Email(message = "{student.email.invalid}")
    private String email;

    @NotNull(message = "{student.birth_date.not_null}")
    @Past(message = "{student.birth_date.must_be_past}")
    private LocalDate birthDate;
}
```

Tại Controller:
```java
@PostMapping
public ResponseEntity<ApiResponse<StudentResponse>> createStudent(
        @Valid @RequestBody CreateStudentRequest request) {
    StudentResponse response = studentService.createStudent(request);
    return ResponseEntity.status(HttpStatus.CREATED)
            .body(ApiResponse.created(MessageConstants.OPERATION_SUCCESS, response));
}
```
