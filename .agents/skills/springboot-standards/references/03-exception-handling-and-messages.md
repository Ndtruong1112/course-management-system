# 03. Xử lý Ngoại lệ & Chuẩn hóa Thông báo Hệ thống

Tài liệu này cung cấp hướng dẫn toàn diện về cơ chế bắt lỗi tập trung (`@RestControllerAdvice`), cấu trúc phản hồi lỗi chuẩn RFC 7807, và **nguyên tắc bắt buộc chuẩn hóa 100% chuỗi thông báo vào package `common`**.

---

## 1. Nguyên tắc cốt lõi: Chuẩn hóa Thông báo tập trung (No Hardcoded Strings)

### Quy tắc bất biến:
- **CẤM:** Viết chuỗi thông báo lỗi hoặc chuỗi phản hồi trực tiếp (hardcoded literal strings) trong Controller, Service, DAO hoặc Entity:
  ```java
  // ANTI-PATTERN: TUYỆT ĐỐI KHÔNG VIẾT NHƯ THẾ NÀY
  throw new ResourceNotFoundException("Không tìm thấy người dùng với ID này");
  throw new BadRequestException("Email đã tồn tại trên hệ thống");
  ```
- **BẮT BUỘC:** Mọi thông báo lỗi, cảnh báo, chuỗi validation và thông báo thành công phải được định nghĩa dưới dạng **hằng số (`public static final String`) hoặc Enum** tại package `common`:
  ```java
  // STANDARD PATTERN: Định nghĩa tại com.company.project.common.MessageConstants
  public final class MessageConstants {
      private MessageConstants() {}
      
      public static final String USER_NOT_FOUND_ID = "Không tìm thấy người dùng với ID: %d";
      public static final String EMAIL_ALREADY_EXISTS = "Email '%s' đã được sử dụng bởi người dùng khác.";
      public static final String OPERATION_SUCCESS = "Thao tác thành công";
      public static final String ACCESS_DENIED = "Truy cập bị từ chối. Bạn không có quyền thực hiện.";
  }
  ```
  Tại tầng Service:
  ```java
  throw new ResourceNotFoundException(String.format(MessageConstants.USER_NOT_FOUND_ID, id));
  ```

---

## 2. Cấu trúc Đối tượng Lỗi chuẩn (`ErrorResponse`)

Mọi lỗi trả về cho Client phải có cấu trúc nhất quán, cung cấp đầy đủ thông tin để Frontend hiển thị và log tracing:

```java
package com.company.project.common.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {

    @Builder.Default
    private LocalDateTime timestamp = LocalDateTime.now();

    private int status;

    private String error;

    private String message;

    private String path;

    // Chứa chi tiết lỗi validation từng trường { "email": "Email không hợp lệ", "age": "Tuổi phải >= 18" }
    private Map<String, String> validationErrors;
}
```

---

## 3. Cây phân cấp Ngoại lệ chuẩn (Exception Hierarchy)

```text
RuntimeException
└── AppException (Lớp cha cho mọi lỗi nghiệp vụ trong hệ thống)
    ├── ResourceNotFoundException (404 NOT FOUND)
    ├── BadRequestException (400 BAD REQUEST)
    ├── ConflictException (409 CONFLICT)
    └── UnauthorizedException (401 UNAUTHORIZED)
```

### Class `AppException` mẫu:
```java
package com.company.project.common.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public class AppException extends RuntimeException {

    private final HttpStatus httpStatus;

    public AppException(String message) {
        super(message);
        this.httpStatus = HttpStatus.BAD_REQUEST;
    }

    public AppException(String message, HttpStatus httpStatus) {
        super(message);
        this.httpStatus = httpStatus;
    }
}
```

---

## 4. Global Exception Handler chuẩn (`@RestControllerAdvice`)

Bộ xử lý lỗi tập trung bắt mọi ngoại lệ phát sinh từ toàn bộ ứng dụng:

```java
package com.company.project.common.exception;

import com.company.project.common.MessageConstants;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    // 1. Bắt lỗi không tìm thấy tài nguyên (404)
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(ResourceNotFoundException ex, HttpServletRequest request) {
        logger.warn("Resource not found: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.NOT_FOUND, ex.getMessage(), request.getRequestURI(), null);
    }

    // 2. Bắt lỗi vi phạm Bean Validation (400)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex, HttpServletRequest request) {
        Map<String, String> errors = new HashMap<>();
        for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {
            errors.put(fieldError.getField(), fieldError.getDefaultMessage());
        }
        logger.warn("Validation failed for URI {}: {}", request.getRequestURI(), errors);
        return buildErrorResponse(HttpStatus.BAD_REQUEST, MessageConstants.BAD_REQUEST, request.getRequestURI(), errors);
    }

    // 3. Bắt lỗi nghiệp vụ chung (AppException / BadRequestException)
    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(BadRequestException ex, HttpServletRequest request) {
        logger.warn("Bad request: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.BAD_REQUEST, ex.getMessage(), request.getRequestURI(), null);
    }

    // 4. Bắt lỗi vi phạm ràng buộc DB (409 Conflict)
    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrity(DataIntegrityViolationException ex, HttpServletRequest request) {
        logger.warn("Data integrity conflict: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.CONFLICT, MessageConstants.DATA_INTEGRITY_VIOLATION, request.getRequestURI(), null);
    }

    // 5. Bắt lỗi ngoài ý muốn (500 Internal Server Error)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUncaughtException(Exception ex, HttpServletRequest request) {
        logger.error("Internal server error occurred at URI {}: ", request.getRequestURI(), ex);
        return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR, MessageConstants.INTERNAL_SERVER_ERROR, request.getRequestURI(), null);
    }

    private ResponseEntity<ErrorResponse> buildErrorResponse(HttpStatus status, String message, String path, Map<String, String> validationErrors) {
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(status.value())
                .error(status.getReasonPhrase())
                .message(message)
                .path(path)
                .validationErrors(validationErrors)
                .build();
        return new ResponseEntity<>(errorResponse, status);
    }
}
```
