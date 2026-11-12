# TOÀN BỘ MÃ NGUỒN DỰ ÁN COURSE MANAGEMENT SYSTEM

Tài liệu này tổng hợp toàn bộ các file Java, Generic DAO, MinIO Storage, JPA Specification và cấu hình để nạp vào Mô hình AI Lớn (Teacher Model) phục vụ Chưng cất Tri thức (Knowledge Distillation).

---

## File: `src/main/java/com/mkii/coursemanagementsystem/CourseManagementSystemApplication.java`

```java
package com.mkii.coursemanagementsystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CourseManagementSystemApplication {

    public static void main(String[] args) {
        SpringApplication.run(CourseManagementSystemApplication.class, args);
    }

}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/ApiConstants.java`

```java
package com.mkii.coursemanagementsystem.common;

public final class ApiConstants {

    private ApiConstants() {
        // Prevent instantiation
    }

    public static final String BASE_COURSE_URL = "/api/courses";
    public static final String BASE_STUDENT_URL = "/api/students";
    public static final String BASE_DOCUMENT_URL = "/api/documents";
    public static final String BASE_SECURITY_URL = "/api/security";
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/MessageConstants.java`

```java
package com.mkii.coursemanagementsystem.common;

public final class MessageConstants {

    private MessageConstants() {
        // Prevent instantiation
    }

    // Generic Entity Validation Messages
    public static final String ENTITY_CANNOT_BE_NULL = "Cannot process a null entity.";
    public static final String CANNOT_CREATE_NULL_ENTITY = "Cannot create null entity[%s]";
    public static final String CANNOT_UPDATE_NULL_ENTITY = "Cannot update null entity[%s]";
    public static final String CANNOT_DELETE_NULL_ENTITY = "Cannot delete null entity[%s]";
    public static final String CANNOT_SAVE_OR_UPDATE_NULL_ENTITY = "Cannot save or update null entity[%s]";
    public static final String CANNOT_DELETE_NULL_ID = "Cannot delete entity with null id[%s]";

    // Business Exception Messages
    public static final String COURSE_NOT_FOUND = "Không tìm thấy khóa học với ID: %d";
    public static final String COURSE_NOT_FOUND_TITLE = "Không tìm thấy khóa học với tiêu đề: %s";
    public static final String COURSE_NOT_FOUND_FIELD = "Không tìm thấy khóa học với %s: %s";
    public static final String STUDENT_NOT_FOUND = "Không tìm thấy sinh viên với ID: %d";
    public static final String STUDENT_NOT_FOUND_EMAIL = "Không tìm thấy sinh viên với email: %s";
    public static final String STUDENT_NOT_FOUND_FIELD = "Không tìm thấy sinh viên với %s: %s";
    public static final String DOCUMENT_NOT_FOUND = "Không tìm thấy tài liệu với ID: %s";
    public static final String FILE_EXTENSION_NOT_SUPPORTED = "Định dạng file không được hỗ trợ. Chỉ chấp nhận: PDF, XLSX, XLS, DOC, DOCX, JPG, JPEG, PNG";
    public static final String INVALID_DOCUMENT = "Tài liệu không tồn tại hoặc không hợp lệ.";
    public static final String SUCCESS_JSON = "{\"status\": \"SUCCESS\", \"message\": \"Thao tác thành công\"}";

    // Standard Success Messages
    public static final String STATUS = "status";
    public static final String SUCCESS = "SUCCESS";
    public static final String MESSAGE = "message";
    public static final String COUNT = "count";
    public static final String TOTAL_INSERTED = "totalInserted";
    public static final String REJECTED = "REJECTED";
    public static final String ACTIVE = "ACTIVE";
    public static final String INACTIVE = "INACTIVE";
    public static final String APP_ID = "appId";
    public static final String USER_APP_ID = "userAppId";
    public static final String ID_FIELD_CANNOT_BE_EMPTY = "ID field cannot be empty.";
    public static final String NO_RECORD_WITH_SUCH_ID = "No record found with ID: %s";
    public static final String COURSE_DELETED_SUCCESS = "Course deleted successfully";
    public static final String COURSE_UPDATED_SUCCESS = "Course updated successfully";
    public static final String STUDENT_DELETED_SUCCESS = "Student deleted successfully";
    public static final String STUDENT_UPDATED_SUCCESS = "Student updated successfully";
    public static final String DOCUMENT_DELETED_SUCCESS = "Deleted successfully";
    public static final String DOCUMENT_RESTORED_SUCCESS = "Khôi phục tài liệu thành công: %s";
    public static final String BATCH_CREATED_SUCCESS = "Batch created successfully";
    public static final String OPERATION_SUCCESS = "Thao tác thành công";

    // Document Validation Messages
    public static final String APP_ID_CANNOT_BE_BLANK = "appId (mã công việc/nghiệp vụ) không được để trống.";
    public static final String FILE_LIST_CANNOT_BE_EMPTY = "Danh sách file tải lên không hợp lệ hoặc để trống.";
    public static final String FILE_CANNOT_BE_EMPTY = "File tải lên không được để trống.";
    public static final String FILE_NAME_SPECIAL_CHAR = "Tên file không được chứa ký tự đặc biệt: %s";
    public static final String FILE_NAME_MAX_LENGTH = "Tên file vượt quá độ dài tối đa 50 ký tự: %s";
    public static final String FILE_PATH_CANNOT_BE_BLANK = "Đường dẫn file không được để trống.";
    public static final String DOCUMENT_NOT_RESTOREABLE = "Tài liệu chưa bị xóa mềm hoặc không tồn tại để khôi phục.";
    public static final String CANNOT_READ_FILE_DATA = "Không thể đọc dữ liệu file: %s";

    // Student Validation Messages
    public static final String EMAIL_ALREADY_EXISTS = "Email '%s' đã được sử dụng bởi sinh viên khác.";

    // Security & Data Processing Messages
    public static final String DATA_TO_ENCRYPT_CANNOT_BE_EMPTY = "Dữ liệu mã hóa không được để trống.";
    public static final String DATA_TO_DECRYPT_CANNOT_BE_EMPTY = "Dữ liệu giải mã không được để trống.";
    public static final String ENCRYPTION_FAILED = "Lỗi khi thực hiện mã hóa dữ liệu: %s";
    public static final String DECRYPTION_FAILED = "Lỗi khi thực hiện giải mã dữ liệu: %s";
    public static final String ACCESS_DENIED = "Truy cập bị từ chối. Bạn không có quyền thực hiện thao tác này.";
    public static final String AUTHENTICATION_REQUIRED = "Yêu cầu xác thực tài khoản để truy cập.";
    public static final String INTERNAL_SERVER_ERROR = "Đã xảy ra lỗi hệ thống, vui lòng thử lại sau.";
    public static final String BAD_REQUEST = "Yêu cầu không hợp lệ.";
    public static final String METHOD_NOT_SUPPORTED = "Phương thức HTTP không được hỗ trợ.";
    public static final String MALFORMED_JSON_REQUEST = "Dữ liệu gửi lên không đúng định dạng JSON.";
    public static final String DATA_INTEGRITY_VIOLATION = "Dữ liệu vi phạm ràng buộc cơ sở dữ liệu (ví dụ: email đã tồn tại).";
    public static final String PARAM_TYPE_MISMATCH = "Tham số '%s' có giá trị '%s' không đúng kiểu dữ liệu yêu cầu";

    // Storage (MinIO) Messages
    public static final String MINIO_CONNECT_FAILED = "Could not connect to MinIO storage: %s";
    public static final String MINIO_UPLOAD_FAILED = "Failed to upload file to MinIO: %s";
    public static final String MINIO_DOWNLOAD_FAILED = "Failed to download file from MinIO: %s";
    public static final String MINIO_DELETE_FAILED = "Failed to delete file from MinIO: %s";
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/converter/AesEncryptConverter.java`

```java
package com.mkii.coursemanagementsystem.common.converter;

import com.mkii.coursemanagementsystem.util.AESUtil;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.crypto.SecretKey;

/**
 * JPA AttributeConverter that automatically encrypts sensitive Entity fields using AES
 * before writing to the database, and transparently decrypts them back upon retrieval.
 */
@Converter
public class AesEncryptConverter implements AttributeConverter<String, String> {

    private static final Logger logger = LoggerFactory.getLogger(AesEncryptConverter.class);
    private static final SecretKey SECRET_KEY;

    static {
        try {
            String key = System.getenv("CMS_AES_KEY") != null
                    ? System.getenv("CMS_AES_KEY") : "CourseManagementSystemSecretKey2026";
            String salt = System.getenv("CMS_AES_SALT") != null
                    ? System.getenv("CMS_AES_SALT") : "cms-salt-2026-v1";
            SECRET_KEY = AESUtil.getKeyFromPassword(key, salt);
        } catch (Exception e) {
            throw new ExceptionInInitializerError("Could not initialize AES SecretKey: " + e.getMessage());
        }
    }

    @Override
    public String convertToDatabaseColumn(String attribute) {
        if (attribute == null || attribute.trim().isEmpty()) {
            return attribute;
        }
        try {
            return AESUtil.encryptStringWithIv(attribute, SECRET_KEY);
        } catch (Exception e) {
            logger.error("Error encrypting entity attribute: {}", e.getMessage());
            return attribute;
        }
    }

    @Override
    public String convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.trim().isEmpty()) {
            return dbData;
        }
        try {
            return AESUtil.decryptStringWithIv(dbData, SECRET_KEY);
        } catch (Exception e) {
            // Graceful fallback for unencrypted legacy / mock data
            return dbData;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/BadRequestException.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

public class BadRequestException extends RuntimeException {

    public BadRequestException(String message) {
        super(message);
    }

    public BadRequestException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/ErrorResponse.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/GlobalExceptionHandler.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

import java.time.LocalDateTime;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException ex, HttpServletRequest request) {
        logger.warn("Resource not found: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.NOT_FOUND.value())
                .error(HttpStatus.NOT_FOUND.getReasonPhrase())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex, HttpServletRequest request) {
        String validationErrors = ex.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining("; "));
        logger.warn("Validation failed: {}", validationErrors);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(validationErrors)
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleTypeMismatchException(MethodArgumentTypeMismatchException ex, HttpServletRequest request) {
        String message = String.format("Tham số '%s' có giá trị '%s' không đúng kiểu dữ liệu yêu cầu", ex.getName(), ex.getValue());
        logger.warn("Type mismatch: {}", message);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(message)
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException ex, HttpServletRequest request) {
        logger.warn("Malformed JSON request: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message("Dữ liệu gửi lên không đúng định dạng JSON.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrityViolationException(DataIntegrityViolationException ex, HttpServletRequest request) {
        logger.warn("Data integrity violation: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.CONFLICT.value())
                .error(HttpStatus.CONFLICT.getReasonPhrase())
                .message("Dữ liệu vi phạm ràng buộc toàn vẹn cơ sở dữ liệu (dữ liệu đang được tham chiếu hoặc giá trị duy nhất đã tồn tại).")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.CONFLICT);
    }

    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<ErrorResponse> handleMissingParams(MissingServletRequestParameterException ex, HttpServletRequest request) {
        logger.warn("Missing parameter: {}", ex.getParameterName());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(String.format("Thiếu tham số bắt buộc '%s' của kiểu %s", ex.getParameterName(), ex.getParameterType()))
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ResponseEntity<ErrorResponse> handleMaxSizeException(MaxUploadSizeExceededException ex, HttpServletRequest request) {
        logger.warn("Max upload size exceeded: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message("Dung lượng file tải lên vượt quá giới hạn tối đa cho phép.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<ErrorResponse> handleMethodNotSupported(HttpRequestMethodNotSupportedException ex, HttpServletRequest request) {
        logger.warn("Method not supported: {}", ex.getMethod());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.METHOD_NOT_ALLOWED.value())
                .error(HttpStatus.METHOD_NOT_ALLOWED.getReasonPhrase())
                .message(String.format("Phương thức HTTP '%s' không được hỗ trợ cho endpoint này.", ex.getMethod()))
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.METHOD_NOT_ALLOWED);
    }

    @ExceptionHandler(NoResourceFoundException.class)
    public ResponseEntity<ErrorResponse> handleNoResourceFound(NoResourceFoundException ex, HttpServletRequest request) {
        logger.warn("Static resource not found: {}", ex.getResourcePath());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.NOT_FOUND.value())
                .error(HttpStatus.NOT_FOUND.getReasonPhrase())
                .message("Tài nguyên không tồn tại: " + ex.getResourcePath())
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler({BadRequestException.class, IllegalArgumentException.class})
    public ResponseEntity<ErrorResponse> handleBadRequestException(Exception ex, HttpServletRequest request) {
        logger.warn("Bad request: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(org.springframework.security.access.AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDeniedException(org.springframework.security.access.AccessDeniedException ex, HttpServletRequest request) {
        logger.warn("Access denied: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.FORBIDDEN.value())
                .error(HttpStatus.FORBIDDEN.getReasonPhrase())
                .message("Truy cập bị từ chối. Bạn không có quyền thực hiện thao tác này.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(org.springframework.security.core.AuthenticationException.class)
    public ResponseEntity<ErrorResponse> handleAuthenticationException(org.springframework.security.core.AuthenticationException ex, HttpServletRequest request) {
        logger.warn("Authentication failed: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.UNAUTHORIZED.value())
                .error(HttpStatus.UNAUTHORIZED.getReasonPhrase())
                .message("Yêu cầu xác thực tài khoản để truy cập.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex, HttpServletRequest request) {
        logger.error("Internal server error: ", ex);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
                .message("Đã xảy ra lỗi hệ thống nội bộ. Vui lòng liên hệ quản trị viên.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/ResourceNotFoundException.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }

    public ResourceNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/ValidationException.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

/**
 * Custom runtime exception thrown when business or data validation fails.
 * Handled globally by {@link GlobalExceptionHandler} to return HTTP 400 (Bad Request).
 */
public class ValidationException extends RuntimeException {

    public ValidationException(String message) {
        super(message);
    }

    public ValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/config/DataInitializer.java`

```java
package com.mkii.coursemanagementsystem.config;

import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.entity.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger logger = LoggerFactory.getLogger(DataInitializer.class);

    private final IDepartmentDao departmentDao;
    private final IUserDao userDao;
    private final ICourseDao courseDao;
    private final IStudentDao studentDao;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(IDepartmentDao departmentDao,
                           IUserDao userDao,
                           ICourseDao courseDao,
                           IStudentDao studentDao,
                           PasswordEncoder passwordEncoder) {
        this.departmentDao = departmentDao;
        this.userDao = userDao;
        this.courseDao = courseDao;
        this.studentDao = studentDao;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional
    public void run(String... args) {
        logger.info("======================================================================");
        logger.info("   KIỂM TRA & KHỞI TẠO DỮ LIỆU MẪU HỆ THỐNG (DATA INITIALIZER)");
        logger.info("======================================================================");

        // 1. Khởi tạo Khoa / Ngành (Departments)
        Department cntt = initDepartment("CNTT", "Công nghệ thông tin", "Khoa Công nghệ thông tin & Truyền thông");
        Department khmt = initDepartment("KHMT", "Khoa học máy tính", "Khoa Khoa học máy tính & Trí tuệ nhân tạo");
        Department qtkd = initDepartment("QTKD", "Quản trị kinh doanh", "Khoa Quản trị kinh doanh & Kinh tế số");

        // 2. Khởi tạo Tài khoản mẫu (Users)
        initUser("admin", "123456", "admin@school.edu.vn", "Quản Trị Viên Hệ Thống", "ADMIN");
        initUser("gv_nam", "123456", "nam@school.edu.vn", "ThS. Nguyễn Văn Nam", "TEACHER");
        initUser("student_a", "123456", "student_a@school.edu.vn", "Nguyễn Văn A", "USER");

        // 3. Khởi tạo Khóa học mẫu (Courses)
        if (courseDao.getCount() == 0) {
            courseDao.save(Course.builder()
                    .title("Lập trình Spring Boot 3 & Hibernate DAO Chuyên Sâu")
                    .description("Khóa học thực chiến từ kiến trúc Generic DAO đến REST API và MinIO")
                    .duration(60)
                    .price(499.0)
                    .build());

            courseDao.save(Course.builder()
                    .title("Xây dựng Trợ lý AI Chuyên Biệt với PyTorch & QLoRA")
                    .description("Tự động tinh chỉnh mô hình mã nguồn mở Qwen trên GPU cục bộ")
                    .duration(45)
                    .price(699.0)
                    .build());

            courseDao.save(Course.builder()
                    .title("Kiến trúc Hệ thống Phân tán & Lưu trữ Đám mây MinIO")
                    .description("Lưu trữ phi cấu trúc, xử lý tệp đa luồng và bảo mật dữ liệu")
                    .duration(30)
                    .price(350.0)
                    .build());
            logger.info("-> Đã khởi tạo 3 khóa học mẫu thành công.");
        }

        // 4. Khởi tạo Sinh viên mẫu (Students)
        if (studentDao.getCount() == 0) {
            studentDao.save(Student.builder()
                    .fullName("Nguyễn Văn A")
                    .email("vana@gmail.com")
                    .phone("0912345678")
                    .address("Hà Nội")
                    .dob(LocalDate.of(2003, 5, 15))
                    .department(cntt)
                    .build());

            studentDao.save(Student.builder()
                    .fullName("Trần Thị B")
                    .email("thib@gmail.com")
                    .phone("0987654321")
                    .address("Đà Nẵng")
                    .dob(LocalDate.of(2004, 8, 20))
                    .department(khmt)
                    .build());

            studentDao.save(Student.builder()
                    .fullName("Lê Văn C")
                    .email("vanc@gmail.com")
                    .phone("0905123456")
                    .address("TP. Hồ Chí Minh")
                    .dob(LocalDate.of(2002, 11, 10))
                    .department(qtkd)
                    .build());
            logger.info("-> Đã khởi tạo 3 sinh viên mẫu có gắn Khoa thành công.");
        }

        logger.info("======================================================================");
        logger.info("   HOÀN TẤT KHỞI TẠO DỮ LIỆU! TÀI KHOẢN MẶC ĐỊNH: admin / 123456");
        logger.info("======================================================================");
    }

    private Department initDepartment(String code, String name, String desc) {
        return departmentDao.findByDepartmentCode(code).orElseGet(() -> {
            Department dept = Department.builder()
                    .departmentCode(code)
                    .departmentName(name)
                    .description(desc)
                    .build();
            Department saved = departmentDao.save(dept);
            logger.info("-> Đã tạo Khoa: {} ({})", name, code);
            return saved;
        });
    }

    private void initUser(String username, String rawPassword, String email, String fullName, String role) {
        if (!userDao.existsByUsername(username)) {
            User user = User.builder()
                    .username(username)
                    .password(passwordEncoder.encode(rawPassword))
                    .email(email)
                    .fullName(fullName)
                    .role(role)
                    .build();
            userDao.save(user);
            logger.info("-> Đã tạo User: {} | Role: {}", username, role);
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/config/MinioConfig.java`

```java
package com.mkii.coursemanagementsystem.config;

import io.minio.MinioClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MinioConfig {

    @Value("${minio.endpoint:http://localhost:9000}")
    private String endpoint;

    @Value("${minio.access-key:minioadmin}")
    private String accessKey;

    @Value("${minio.secret-key:minioadmin}")
    private String secretKey;

    @Bean
    public MinioClient minioClient() {
        return MinioClient.builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/config/OpenApiConfig.java`

```java
package com.mkii.coursemanagementsystem.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    public static final String BEARER_AUTH = "bearerAuth";
    public static final String BASIC_AUTH = "basicAuth";
    public static final String SECURITY_SCHEME_NAME = BASIC_AUTH;

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Course Management System API")
                        .version("1.0.0")
                        .description("REST API documentation for Course Management System with Spring Security, JWT, AES Encryption, Generic DAO and MinIO Storage")
                        .contact(new Contact().name("MKII Development Team").email("support@mkii.com"))
                        .license(new License().name("Apache 2.0").url("https://www.apache.org/licenses/LICENSE-2.0.html")))
                .addSecurityItem(new SecurityRequirement().addList(BEARER_AUTH))
                .components(new Components()
                        .addSecuritySchemes(BEARER_AUTH, new SecurityScheme()
                                .name(BEARER_AUTH)
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")
                                .description("JWT Token Authorization: Bearer <token>"))
                        .addSecuritySchemes(BASIC_AUTH, new SecurityScheme()
                                .name(BASIC_AUTH)
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("basic")
                                .description("HTTP Basic Authentication")));
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/config/SecurityConfig.java`

```java
package com.mkii.coursemanagementsystem.config;

import com.mkii.coursemanagementsystem.security.jwt.JwtAccessDeniedHandler;
import com.mkii.coursemanagementsystem.security.jwt.JwtAuthenticationEntryPoint;
import com.mkii.coursemanagementsystem.security.jwt.JwtAuthenticationFilter;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import com.mkii.coursemanagementsystem.security.service.UserDetailsServiceImpl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    private final UserDetailsServiceImpl userDetailsService;
    private final JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint;
    private final JwtAccessDeniedHandler jwtAccessDeniedHandler;
    private final JwtTokenProvider jwtTokenProvider;

    public SecurityConfig(@Lazy UserDetailsServiceImpl userDetailsService,
                          JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint,
                          JwtAccessDeniedHandler jwtAccessDeniedHandler,
                          JwtTokenProvider jwtTokenProvider) {
        this.userDetailsService = userDetailsService;
        this.jwtAuthenticationEntryPoint = jwtAuthenticationEntryPoint;
        this.jwtAccessDeniedHandler = jwtAccessDeniedHandler;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(List.of("*"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type", "X-Requested-With", "Accept", "Origin"));
        configuration.setExposedHeaders(Arrays.asList("Authorization", "Content-Type"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(jwtAuthenticationEntryPoint)
                .accessDeniedHandler(jwtAccessDeniedHandler)
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authorizeHttpRequests(auth -> auth
                // Public giao diện Web tĩnh (Frontend)
                .requestMatchers("/", "/index.html", "/favicon.ico", "/*.html", "/*.css", "/*.js", "/static/**", "/error").permitAll()
                // Public tài liệu Swagger / OpenAPI
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**", "/swagger-ui.html", "/swagger-resources/**", "/webjars/**").permitAll()
                // Public các API xác thực (Đăng nhập, Đăng ký)
                .requestMatchers("/api/auth/**").permitAll()
                // Cho phép xem thông tin khóa học và khoa công khai không cần token (A3)
                .requestMatchers(HttpMethod.GET, "/api/courses/**", "/api/departments/**").permitAll()
                // Cho phép CORS preflight
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                // Quyền ghi đối với khóa học và khoa (ADMIN, TEACHER, LECTURER) (A4)
                .requestMatchers(HttpMethod.POST, "/api/courses/**", "/api/departments/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.PUT, "/api/courses/**", "/api/departments/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.DELETE, "/api/courses/**", "/api/departments/**").hasRole("ADMIN")
                // Quyền ghi đối với sinh viên
                .requestMatchers(HttpMethod.POST, "/api/students/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.PUT, "/api/students/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.DELETE, "/api/students/**").hasRole("ADMIN")
                // Mọi thao tác khác (kể cả GET sinh viên PII, GET/POST tài liệu nội bộ) bắt buộc phải đăng nhập (A3, A4)
                .anyRequest().authenticated()
            );

        JwtAuthenticationFilter jwtAuthenticationFilter = new JwtAuthenticationFilter(jwtTokenProvider, userDetailsService);
        http.authenticationProvider(authenticationProvider());
        http.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/ICourseDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Course;

import java.util.List;

public interface ICourseDao extends IPaginationSortingDao<Long, Course> {

    Course save(Course course);

    Course update(Course course);

    void delete(Long id);

    Course getById(Long id);

    Course getByTitle(String title);

    List<Course> getAll();

    List<Course> searchByTitle(String keyword);

    List<Course> findByPriceRange(Double minPrice, Double maxPrice);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IDepartmentDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Department;

import java.util.List;
import java.util.Optional;

public interface IDepartmentDao extends IPaginationSortingDao<Long, Department> {

    Department save(Department department);

    Department update(Department department);

    void delete(Long id);

    Department getById(Long id);

    Optional<Department> findByDepartmentCode(String departmentCode);

    List<Department> getAll();

    List<Department> searchByName(String keyword);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IDocumentDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;

import java.util.List;

public interface IDocumentDao extends IPaginationSortingDao<String, Document> {

    Document save(Document document);

    Document update(Document document);

    void delete(String id);

    Document getById(String id);

    Document findByPk(String id);

    Document getDocumentName(String fileName, String appId);

    List<Document> getDocumentByAppId(String appId);

    List<Document> findByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IGenericDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Base Generic DAO interface defining standard CRUD and basic query operations.
 * Keeping this interface clean and focused purely on core entity persistence.
 */
public interface IGenericDao<Pk, Entity> {

    @Transactional
    Entity create(Entity anEntity);

    @Transactional
    Entity update(Entity anEntity);

    @Transactional
    Entity saveOrUpdate(Entity anEntity);

    @Transactional
    void delete(Entity anEntity);

    @Transactional
    void deleteById(Pk id);

    void deleteByPk(Pk id);

    Entity get(Pk id);

    Optional<Entity> findById(Pk id);

    Entity getByField(String fieldName, Object value);

    List<Entity> findByField(String fieldName, Object value);

    List<Entity> getAll();

    @Transactional
    List<Entity> createAll(List<Entity> entities);

    @Transactional
    void deleteAll(List<Entity> entities);

    boolean exists(Pk id);

    long count();

    void flush();

    void clear();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IPaginationSortingDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.List;

/**
 * Interface extending {@link IGenericDao} dedicated to Sorting, Pagination,
 * and Dynamic Specification Search.
 */
public interface IPaginationSortingDao<Pk, Entity> extends IGenericDao<Pk, Entity> {

    /** Get all records sorted by a field name and direction ("asc" / "desc"). */
    List<Entity> findAllSorted(String sortBy, String direction);

    /** Get a single page of records, sorted. */
    Page<Entity> findAllPaged(int page, int size, String sortBy, String direction);

    /** Find all records matching a field value, applying Sort. */
    List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort);

    /** Find all records matching a field value, sorted by string parameters. */
    List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction);

    /** Find all records matching a field value, with full Pageable (page + size + sort). */
    Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable);

    /** Find all records matching a field value with pagination and sorting via string parameters. */
    Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction);

    /** Search by query string (key:op:value) using Specification. */
    List<Entity> searchBySpecification(String search);

    /** Search by query string using Specification combined with sorting. */
    List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Search by query string using Specification combined with pagination and sorting. */
    Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    /** Raw Spring Data Specification search without paging. */
    List<Entity> findAll(Specification<Entity> spec);

    /** Raw Spring Data Specification search with paging. */
    Page<Entity> findAll(Specification<Entity> spec, Pageable pageable);

    /** Raw Spring Data Specification search with sort. */
    List<Entity> findAll(Specification<Entity> spec, Sort sort);

    Page<Entity> getAll(Pageable pageable);

    List<Entity> getAll(Sort sort);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IStudentDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Student;

import java.util.List;
import java.util.Optional;

public interface IStudentDao extends IPaginationSortingDao<Long, Student> {

    Student save(Student student);

    Student update(Student student);

    void delete(Long id);

    Student getById(Long id);

    Student getByEmail(String email);

    Optional<Student> findByEmail(String email);

    List<Student> getAll();

    List<Student> searchByKeyword(String keyword);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IUserDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.User;

import java.util.List;
import java.util.Optional;

public interface IUserDao extends IPaginationSortingDao<Long, User> {

    User save(User user);

    User update(User user);

    void delete(Long id);

    User getById(Long id);

    Optional<User> findByUsername(String username);

    Optional<User> findByEmail(String email);

    boolean existsByUsername(String username);

    boolean existsByEmail(String email);

    List<User> getAll();

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/CourseDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;

@Repository
public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {

    private static final Logger logger = LoggerFactory.getLogger(CourseDaoImpl.class);

    public CourseDaoImpl(EntityManager entityManager) {
        super(Course.class, entityManager);
    }

    @Override
    public Course save(Course course) {
        logger.info("Saving Course: {}", course.getTitle());
        return super.save(course);
    }

    @Override
    public Course update(Course course) {
        logger.info("Updating Course: {}", course.getId());
        return super.update(course);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Course: {}", id);
        deleteByPk(id);
    }

    @Override
    public Course getById(Long id) {
        logger.info("Getting Course by id: {}", id);
        return get(id);
    }

    @Override
    public Course getByTitle(String title) {
        logger.info("Getting Course by title: {}", title);
        return getByField("title", title);
    }

    @Override
    public List<Course> getAll() {
        logger.info("Getting all Courses");
        return findAll(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "id"));
    }

    @Override
    public List<Course> searchByTitle(String keyword) {
        logger.info("Searching Courses by title keyword: {}", keyword);
        return findByHql(
                "SELECT c FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%'))",
                java.util.Map.of("keyword", keyword)
        );
    }

    @Override
    public List<Course> findByPriceRange(Double minPrice, Double maxPrice) {
        logger.info("Getting Courses by price range: {} - {}", minPrice, maxPrice);
        return findByHql(
                "SELECT c FROM Course c WHERE c.price BETWEEN :minPrice AND :maxPrice",
                java.util.Map.of("minPrice", minPrice, "maxPrice", maxPrice)
        );
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Course count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/DepartmentDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Repository
public class DepartmentDaoImpl extends HibernatePaginationSortingDao<Long, Department> implements IDepartmentDao {

    private static final Logger logger = LoggerFactory.getLogger(DepartmentDaoImpl.class);

    public DepartmentDaoImpl(EntityManager entityManager) {
        super(Department.class, entityManager);
    }

    @Override
    public Department save(Department department) {
        logger.info("Saving Department: {}", department.getDepartmentCode());
        return super.save(department);
    }

    @Override
    public Department update(Department department) {
        logger.info("Updating Department: {}", department.getDepartmentId());
        return super.update(department);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Department: {}", id);
        deleteByPk(id);
    }

    @Override
    public Department getById(Long id) {
        logger.info("Getting Department by ID: {}", id);
        return get(id);
    }

    @Override
    public Optional<Department> findByDepartmentCode(String departmentCode) {
        logger.info("Finding Department by code: {}", departmentCode);
        String hql = "SELECT d FROM Department d WHERE d.departmentCode = :code";
        TypedQuery<Department> query = entityManager.createQuery(hql, Department.class);
        query.setParameter("code", departmentCode);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public List<Department> getAll() {
        logger.info("Fetching all departments");
        return findAll();
    }

    @Override
    public List<Department> searchByName(String keyword) {
        logger.info("Searching departments by keyword: {}", keyword);
        if (keyword == null || keyword.trim().isEmpty()) {
            return Collections.emptyList();
        }
        String hql = "SELECT d FROM Department d WHERE LOWER(d.departmentName) LIKE LOWER(:keyword) OR LOWER(d.departmentCode) LIKE LOWER(:keyword)";
        TypedQuery<Department> query = entityManager.createQuery(hql, Department.class);
        query.setParameter("keyword", "%" + keyword.trim() + "%");
        return query.getResultList();
    }

    @Override
    public Integer getCount() {
        logger.info("Getting total departments count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/DocumentDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class DocumentDaoImpl extends HibernatePaginationSortingDao<String, Document> implements IDocumentDao {

    private static final Logger logger = LoggerFactory.getLogger(DocumentDaoImpl.class);

    public DocumentDaoImpl(EntityManager entityManager) {
        super(Document.class, entityManager);
    }

    @Override
    public Document save(Document document) {
        logger.info("Saving Document: name={}, appId={}", document.getName(), document.getAppId());
        return super.save(document);
    }

    @Override
    public Document update(Document document) {
        logger.info("Updating Document: id={}", document.getId());
        return super.update(document);
    }

    @Override
    public void delete(String id) {
        logger.info("Deleting Document: id={}", id);
        deleteByPk(id);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting Document by id: {}", id);
        return get(id);
    }

    @Override
    public Document findByPk(String id) {
        logger.info("Finding Document by pk: {}", id);
        return get(id);
    }

    @Override
    public Document getDocumentName(String fileName, String appId) {
        logger.info("document name: {} for appId: {}", fileName, appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByName", Document.class)
                    .setParameter("name", fileName)
                    .setParameter("appId", appId);
            List<Document> list = query.setMaxResults(1).getResultList();
            return list.isEmpty() ? null : list.get(0);
        } catch (Exception e) {
            logger.error("Error executing getDocumentByName: {}", e.getMessage());
            return null;
        }
    }

    @Override
    public List<Document> getDocumentByAppId(String appId) {
        logger.info("Inside getDocumentByAppId appId: {}", appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByAppId", Document.class)
                    .setParameter("appId", appId);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error executing getDocumentByAppId: {}", e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public List<Document> findByAppId(String appId) {
        return getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active Documents");
        return findByHql(
                "SELECT d FROM Document d WHERE d.deleted = false ORDER BY d.creationTime DESC",
                null
        );
    }

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);

        int offset = (lowerLimit != null && lowerLimit >= 0) ? lowerLimit : 0;
        int limit = (upperLimit != null && upperLimit > 0) ? upperLimit : 10;
        String sortField = (orderBy != null && !orderBy.isBlank()) ? orderBy : "creationTime";
        String direction = (orderType != null && !orderType.isBlank()) ? orderType : "desc";

        StringBuilder jpql = new StringBuilder("SELECT d FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        Sort sort = buildSort(sortField, direction);
        jpql.append(buildOrderClause("d", sort));

        TypedQuery<Document> typedQuery = getEntityManager().createQuery(jpql.toString(), Document.class);
        params.forEach(typedQuery::setParameter);
        typedQuery.setFirstResult(offset);
        typedQuery.setMaxResults(limit);

        return typedQuery.getResultList();
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("getDocCount: query={}, appId={}", query, appId);

        StringBuilder jpql = new StringBuilder("SELECT COUNT(d) FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        TypedQuery<Long> countQuery = getEntityManager().createQuery(jpql.toString(), Long.class);
        params.forEach(countQuery::setParameter);

        Long count = countQuery.getSingleResult();
        return count != null ? count.intValue() : 0;
    }

    @Override
    public Page<Document> findAllPaged(int page, int size, String sortBy, String direction) {
        Sort sort = buildSort(sortBy, direction);
        Pageable pageable = PageRequest.of(page, size, sort);
        String countJpql = "SELECT COUNT(d) FROM Document d WHERE d.deleted = false";
        Long total = getEntityManager().createQuery(countJpql, Long.class).getSingleResult();
        if (total == null || total == 0) {
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
        String orderClause = buildOrderClause("d", sort);
        String jpql = "SELECT d FROM Document d WHERE d.deleted = false" + orderClause;
        List<Document> content = getEntityManager().createQuery(jpql, Document.class)
                .setFirstResult((int) pageable.getOffset())
                .setMaxResults(pageable.getPageSize())
                .getResultList();
        return new PageImpl<>(content, pageable, total);
    }

    @Override
    public List<Document> findAllSorted(String sortBy, String direction) {
        Sort sort = buildSort(sortBy, direction);
        String orderClause = buildOrderClause("d", sort);
        String jpql = "SELECT d FROM Document d WHERE d.deleted = false" + orderClause;
        return getEntityManager().createQuery(jpql, Document.class).getResultList();
    }

    @Override
    public Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("findByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        Pageable pageable = PageRequest.of(page, size, sort);
        String countJpql = "SELECT COUNT(d) FROM Document d WHERE d.appId = :appId AND d.deleted = false";
        Long total = getEntityManager().createQuery(countJpql, Long.class)
                .setParameter("appId", appId)
                .getSingleResult();
        if (total == null || total == 0) {
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
        String orderClause = buildOrderClause("d", sort);
        String jpql = "SELECT d FROM Document d WHERE d.appId = :appId AND d.deleted = false" + orderClause;
        List<Document> content = getEntityManager().createQuery(jpql, Document.class)
                .setParameter("appId", appId)
                .setFirstResult((int) pageable.getOffset())
                .setMaxResults(pageable.getPageSize())
                .getResultList();
        return new PageImpl<>(content, pageable, total);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/StudentDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Repository
public class StudentDaoImpl extends HibernatePaginationSortingDao<Long, Student> implements IStudentDao {

    private static final Logger logger = LoggerFactory.getLogger(StudentDaoImpl.class);

    public StudentDaoImpl(EntityManager entityManager) {
        super(Student.class, entityManager);
    }

    @Override
    public Student save(Student student) {
        logger.info("Saving Student: {}", student.getFullName());
        return super.save(student);
    }

    @Override
    public Student update(Student student) {
        logger.info("Updating Student: {}", student.getId());
        return super.update(student);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        deleteByPk(id);
    }

    @Override
    public Student getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        return get(id);
    }

    @Override
    public Student getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        return getByField("email", email);
    }

    @Override
    public Optional<Student> findByEmail(String email) {
        logger.info("Getting Student optional by email: {}", email);
        return Optional.ofNullable(getByField("email", email));
    }

    @Override
    public List<Student> getAll() {
        logger.info("Getting all Students");
        return findAll(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "id"));
    }

    @Override
    public List<Student> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return findByHql(
                "SELECT s FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :keyword, '%'))",
                java.util.Map.of("keyword", keyword)
        );
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/UserDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.entity.User;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public class UserDaoImpl extends HibernatePaginationSortingDao<Long, User> implements IUserDao {

    private static final Logger logger = LoggerFactory.getLogger(UserDaoImpl.class);

    public UserDaoImpl(EntityManager entityManager) {
        super(User.class, entityManager);
    }

    @Override
    public User save(User user) {
        logger.info("Saving User: {}", user.getUsername());
        return super.save(user);
    }

    @Override
    public User update(User user) {
        logger.info("Updating User: {}", user.getUserId());
        return super.update(user);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting User: {}", id);
        deleteByPk(id);
    }

    @Override
    public User getById(Long id) {
        logger.info("Getting User by ID: {}", id);
        return get(id);
    }

    @Override
    public Optional<User> findByUsername(String username) {
        logger.info("Finding User by username: {}", username);
        String hql = "SELECT u FROM User u WHERE u.username = :username";
        TypedQuery<User> query = entityManager.createQuery(hql, User.class);
        query.setParameter("username", username);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public Optional<User> findByEmail(String email) {
        logger.info("Finding User by email: {}", email);
        String hql = "SELECT u FROM User u WHERE u.email = :email";
        TypedQuery<User> query = entityManager.createQuery(hql, User.class);
        query.setParameter("email", email);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public boolean existsByUsername(String username) {
        String hql = "SELECT COUNT(u) FROM User u WHERE u.username = :username";
        TypedQuery<Long> query = entityManager.createQuery(hql, Long.class);
        query.setParameter("username", username);
        return query.getSingleResult() > 0;
    }

    @Override
    public boolean existsByEmail(String email) {
        String hql = "SELECT COUNT(u) FROM User u WHERE u.email = :email";
        TypedQuery<Long> query = entityManager.createQuery(hql, Long.class);
        query.setParameter("email", email);
        return query.getSingleResult() > 0;
    }

    @Override
    public List<User> getAll() {
        logger.info("Fetching all users");
        return findAll();
    }

    @Override
    public Integer getCount() {
        logger.info("Getting total users count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/CourseRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseRequestDTO {

    @NotBlank(message = "Tiêu đề khóa học không được để trống")
    @Size(max = 255, message = "Tiêu đề khóa học không được vượt quá 255 ký tự")
    private String title;

    private String description;

    @NotNull(message = "Thời lượng khóa học không được để trống")
    @PositiveOrZero(message = "Thời lượng khóa học phải lớn hơn hoặc bằng 0")
    private Integer duration;

    @NotNull(message = "Học phí khóa học không được để trống")
    @PositiveOrZero(message = "Học phí khóa học phải lớn hơn hoặc bằng 0")
    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/CourseResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseResponseDTO {
    private Long id;
    private String title;
    private String description;
    private Integer duration;
    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/DecryptRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Request DTO for data decryption")
public class DecryptRequestDTO {

    @NotBlank(message = "Encrypted data to decrypt cannot be blank")
    @ApiModelProperty(value = "Base64 encoded encrypted ciphertext with prepended IV", required = true)
    private String encryptedData;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/DecryptResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Response DTO for data decryption")
public class DecryptResponseDTO {

    @ApiModelProperty(value = "Decrypted original plaintext string")
    private String decryptedData;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/DepartmentRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DepartmentRequestDTO {

    @NotBlank(message = "Department code is mandatory")
    @Size(max = 20, message = "Department code must not exceed 20 characters")
    private String departmentCode;

    @NotBlank(message = "Department name is mandatory")
    @Size(max = 100, message = "Department name must not exceed 100 characters")
    private String departmentName;

    @Size(max = 255, message = "Description must not exceed 255 characters")
    private String description;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/DepartmentResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DepartmentResponseDTO {

    private Long departmentId;
    private String departmentCode;
    private String departmentName;
    private String description;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updatedAt;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/EncryptRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Request DTO for data encryption")
public class EncryptRequestDTO {

    @NotBlank(message = "Data to encrypt cannot be blank")
    @ApiModelProperty(value = "Plaintext string data to encrypt", required = true, example = "SensitiveStudentData123")
    private String data;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/EncryptResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Response DTO for data encryption")
public class EncryptResponseDTO {

    @ApiModelProperty(value = "Base64 encoded encrypted ciphertext with prepended IV")
    private String encryptedData;

    @ApiModelProperty(value = "Encryption algorithm used", example = "AES/CBC/PKCS5Padding")
    private String algorithm;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/StudentRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentRequestDTO {

    @NotBlank(message = "Họ và tên không được để trống")
    @Size(max = 150, message = "Họ và tên không được vượt quá 150 ký tự")
    private String fullName;

    @NotBlank(message = "Email không được để trống")
    @Email(message = "Email không đúng định dạng")
    @Size(max = 150, message = "Email không được vượt quá 150 ký tự")
    private String email;

    @Pattern(regexp = "^$|[0-9]{10,11}", message = "Số điện thoại phải từ 10-11 chữ số")
    private String phone;

    @Size(max = 255, message = "Địa chỉ không được vượt quá 255 ký tự")
    private String address;

    private java.time.LocalDate dob;

    private Long departmentId;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/StudentResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentResponseDTO {
    private Long id;
    private String fullName;
    private String email;
    private String phone;
    private String address;
    private java.time.LocalDate dob;
    private DepartmentResponseDTO department;

    public StudentResponseDTO(Long id, String fullName, String email, String phone, String address) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
        this.address = address;
    }

    public StudentResponseDTO(Long id, String fullName, String email, String phone, String address, java.time.LocalDate dob) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
        this.address = address;
        this.dob = dob;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/auth/AuthResponse.java`

```java
package com.mkii.coursemanagementsystem.dto.auth;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AuthResponse {

    private String token;
    @Builder.Default
    private String type = "Bearer";
    private Long userId;
    private String username;
    private String email;
    private String fullName;
    private String role;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/auth/LoginRequest.java`

```java
package com.mkii.coursemanagementsystem.dto.auth;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoginRequest {

    @NotBlank(message = "Username không được để trống")
    private String username;

    @NotBlank(message = "Password không được để trống")
    private String password;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/auth/RegisterRequest.java`

```java
package com.mkii.coursemanagementsystem.dto.auth;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RegisterRequest {

    @NotBlank(message = "Username không được để trống")
    @Size(min = 3, max = 50, message = "Username phải từ 3 đến 50 ký tự")
    private String username;

    @NotBlank(message = "Password không được để trống")
    @Size(min = 6, message = "Password phải từ 6 ký tự trở lên")
    private String password;

    @Email(message = "Email không đúng định dạng")
    private String email;

    private String fullName;

    private String role; // "USER", "TEACHER", "ADMIN"
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Course.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "courses", indexes = {
        @Index(name = "idx_course_title", columnList = "title"),
        @Index(name = "idx_course_price", columnList = "price")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    private Integer duration;

    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Department.java`

```java
package com.mkii.coursemanagementsystem.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "departments", indexes = {
        @Index(name = "idx_department_code", columnList = "department_code"),
        @Index(name = "idx_department_name", columnList = "department_name")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Department {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    @Column(name = "department_id")
    private Long departmentId;

    @Column(name = "department_code", length = 20, unique = true, nullable = false)
    private String departmentCode;

    @Column(name = "department_name", length = 100, nullable = false)
    private String departmentName;

    @Column(name = "description", length = 255)
    private String description;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updatedAt;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Document.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;
import java.util.UUID;

@NamedQuery(
        name = "getDocumentByName",
        query = "SELECT d FROM Document d WHERE d.name = :name AND d.deleted = false AND d.active = true AND d.appId = :appId"
)
@NamedQuery(
        name = "getDocumentByAppId",
        query = "SELECT d FROM Document d WHERE d.appId = :appId AND d.deleted = false ORDER BY d.creationTime DESC"
)
@Entity
@Table(name = "documents", indexes = {
        @Index(name = "idx_doc_app_id", columnList = "APP_DETAIL_FK"),
        @Index(name = "idx_doc_name", columnList = "NAME"),
        @Index(name = "idx_doc_deleted", columnList = "DELETED"),
        @Index(name = "idx_doc_active", columnList = "ACTIVE")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "ID", updatable = false, nullable = false, length = 36)
    @EqualsAndHashCode.Include
    private String id;

    @Column(name = "APP_DETAIL_FK", nullable = false)
    private String appId;

    @Column(name = "NAME")
    private String name;

    @Column(name = "PATH")
    private String path;

    @Column(name = "OWNER")
    private String owner;

    @Column(name = "VERSION")
    private Double version;

    @Column(name = "DELETED")
    private Boolean deleted;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "CREATED_TIME")
    private Date creationTime;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "MODIFIED_TIME")
    private Date modificationTime;

    @Column(name = "ACTIVE")
    private Boolean active;

    @PrePersist
    void onCreate() {
        if (this.id == null || this.id.isBlank()) {
            this.id = UUID.randomUUID().toString();
        }
        Date now = new Date();
        this.creationTime = now;
        this.modificationTime = now;
        if (this.deleted == null) {
            this.deleted = false;
        }
        if (this.active == null) {
            this.active = true;
        }
        if (this.version == null) {
            this.version = 1.0;
        }
    }

    @PreUpdate
    void onPersist() {
        this.modificationTime = new Date();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Student.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "students", indexes = {
        @Index(name = "idx_student_email", columnList = "email"),
        @Index(name = "idx_student_fullname", columnList = "fullName")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 150)
    private String fullName;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    @Column(length = 20)
    private String phone;

    @Column(length = 255)
    private String address;

    @Column(name = "dob")
    private java.time.LocalDate dob;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "department_id")
    private Department department;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/User.java`

```java
package com.mkii.coursemanagementsystem.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "users", indexes = {
        @Index(name = "idx_user_username", columnList = "username"),
        @Index(name = "idx_user_email", columnList = "email")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    @Column(name = "user_id")
    private Long userId;

    @Column(name = "username", unique = true, nullable = false, length = 50)
    private String username;

    @Column(name = "password", nullable = false, length = 100)
    private String password;

    @Column(name = "email", length = 100)
    private String email;

    @Column(name = "full_name", length = 100)
    private String fullName;

    @Column(name = "role", length = 20)
    @Builder.Default
    private String role = "USER"; // "ADMIN", "TEACHER", "USER"

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updatedAt;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/hibernateDao/HibernateGenericDao.java`

```java
package com.mkii.coursemanagementsystem.hibernateDao;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.dao.IGenericDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.Query;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.jpa.repository.support.SimpleJpaRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Base Hibernate Generic DAO providing standard CRUD and basic JPQL operations.
 * Kept concise and clean. Advanced Pagination & Sorting has been separated into
 * {@link HibernatePaginationSortingDao}.
 */
public class HibernateGenericDao<Pk, Entity> extends SimpleJpaRepository<Entity, Pk> implements IGenericDao<Pk, Entity> {

    private static final Logger logger = LoggerFactory.getLogger(HibernateGenericDao.class);

    protected Class<Entity> type;
    protected EntityManager entityManager;

    public HibernateGenericDao(Class<Entity> type, EntityManager entityManager) {
        super(type, entityManager);
        this.type = type;
        this.entityManager = entityManager;
    }

    public Class<Entity> getType() {
        return type;
    }

    public void setType(Class<Entity> type) {
        this.type = type;
    }

    public EntityManager getEntityManager() {
        return entityManager;
    }

    public void setEntityManager(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    // ──────────── CRUD Operations ────────────

    @Override
    @Transactional
    public Entity create(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_CREATE_NULL_ENTITY, getType().getName()));
        }
        return super.save(anEntity);
    }

    @Override
    @Transactional
    public Entity update(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_UPDATE_NULL_ENTITY, getType().getName()));
        }
        return saveAndFlush(anEntity);
    }

    @Override
    @Transactional
    public Entity saveOrUpdate(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_SAVE_OR_UPDATE_NULL_ENTITY, getType().getName()));
        }
        return super.save(anEntity);
    }

    @Override
    @Transactional
    public void delete(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_DELETE_NULL_ENTITY, getType().getName()));
        }
        super.delete(anEntity);
    }

    @Override
    @Transactional
    public void deleteById(Pk id) {
        if (id == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_DELETE_NULL_ID, getType().getName()));
        }
        super.deleteById(id);
    }

    @Override
    @Transactional
    public void deleteByPk(Pk id) {
        deleteById(id);
    }

    // ──────────── Basic Queries ────────────

    @Override
    public Entity get(Pk id) {
        if (id == null) {
            return null;
        }
        return super.findById(id).orElse(null);
    }

    @Override
    public Optional<Entity> findById(Pk id) {
        if (id == null) {
            return Optional.empty();
        }
        return super.findById(id);
    }

    @Override
    public Entity getByField(String fieldName, Object value) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return null;
        }
        logger.info("Getting {} by field: {} = {}", getType().getSimpleName(), fieldName, value);
        try {
            String jpql = "SELECT e FROM " + getType().getSimpleName() + " e WHERE e." + fieldName + " = :value";
            TypedQuery<Entity> query = entityManager.createQuery(jpql, getType());
            query.setParameter("value", value);
            List<Entity> results = query.setMaxResults(1).getResultList();
            return results.isEmpty() ? null : results.get(0);
        } catch (Exception e) {
            logger.error("Error getting {} by field {}: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return null;
        }
    }

    @Override
    public List<Entity> findByField(String fieldName, Object value) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return Collections.emptyList();
        }
        logger.info("Finding {} list by field: {} = {}", getType().getSimpleName(), fieldName, value);
        try {
            String jpql = "SELECT e FROM " + getType().getSimpleName() + " e WHERE e." + fieldName + " = :value";
            TypedQuery<Entity> query = entityManager.createQuery(jpql, getType());
            query.setParameter("value", value);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error finding {} by field {}: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return Collections.emptyList();
        }
    }

    protected boolean isValidIdentifier(String identifier) {
        return identifier != null && identifier.matches("^[a-zA-Z0-9_]+$");
    }

    @Override
    public List<Entity> getAll() {
        return findAll();
    }

    @Override
    @Transactional
    public List<Entity> createAll(List<Entity> entities) {
        if (entities == null || entities.isEmpty()) {
            return Collections.emptyList();
        }
        return saveAll(entities);
    }

    @Override
    @Transactional
    public void deleteAll(List<Entity> entities) {
        if (entities == null || entities.isEmpty()) {
            return;
        }
        super.deleteAll(entities);
    }

    // ──────────── Utility ────────────

    @Override
    public boolean exists(Pk id) {
        if (id == null) {
            return false;
        }
        return existsById(id);
    }

    @Override
    public long count() {
        return super.count();
    }

    @Override
    public void flush() {
        super.flush();
    }

    @Override
    public void clear() {
        if (entityManager != null) {
            entityManager.clear();
        }
    }

    // ──────────── JPQL / HQL Helper Methods ────────────

    public List<Entity> findByHql(String hql, Map<String, Object> params) {
        TypedQuery<Entity> query = entityManager.createQuery(hql, getType());
        if (params != null) {
            params.forEach(query::setParameter);
        }
        return query.getResultList();
    }

    @Transactional
    public int executeHql(String hql, Map<String, Object> params) {
        Query query = entityManager.createQuery(hql);
        if (params != null) {
            params.forEach(query::setParameter);
        }
        return query.executeUpdate();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/hibernateDao/HibernatePaginationSortingDao.java`

```java
package com.mkii.coursemanagementsystem.hibernateDao;

import com.mkii.coursemanagementsystem.dao.IPaginationSortingDao;
import com.mkii.coursemanagementsystem.specification.GenericSpecificationsBuilder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.Collections;
import java.util.List;

/**
 * Specialized DAO implementation extending {@link HibernateGenericDao} that houses
 * all Sorting, Pagination, and Specification-based query logic.
 * Keeps HibernateGenericDao lean and modular.
 */
public class HibernatePaginationSortingDao<Pk, Entity> extends HibernateGenericDao<Pk, Entity> implements IPaginationSortingDao<Pk, Entity> {

    private static final Logger logger = LoggerFactory.getLogger(HibernatePaginationSortingDao.class);

    public HibernatePaginationSortingDao(Class<Entity> type, EntityManager entityManager) {
        super(type, entityManager);
    }

    // ──────────── Sorting / Pagination Methods ────────────

    @Override
    public List<Entity> findAllSorted(String sortBy, String direction) {
        logger.info("Finding all {} sorted by {} {}", getType().getSimpleName(), sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        return findAll(sort);
    }

    @Override
    public Page<Entity> findAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Finding all {} paged: page={}, size={}, sort={} {}", getType().getSimpleName(), page, size, sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        Pageable pageable = PageRequest.of(page, size, sort);
        return findAll(pageable);
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return Collections.emptyList();
        }
        logger.info("Finding {} by field {} = {} with sort {}", getType().getSimpleName(), fieldName, value, sort);
        try {
            String orderClause = buildOrderClause(sort);
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            TypedQuery<Entity> query = getEntityManager().createQuery(jpql, getType());
            query.setParameter("value", value);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error finding {} by field {} sorted: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
        logger.info("Finding {} by field {} = {} paged: page={}, size={}", getType().getSimpleName(), fieldName, value, pageable.getPageNumber(), pageable.getPageSize());
        try {
            // Count query
            String countJpql = "SELECT COUNT(e) FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value";
            Long total = getEntityManager().createQuery(countJpql, Long.class)
                    .setParameter("value", value)
                    .getSingleResult();

            if (total == null || total == 0) {
                return new PageImpl<>(Collections.emptyList(), pageable, 0);
            }

            // Data query with order and pagination
            String orderClause = buildOrderClause(pageable.getSort());
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            List<Entity> content = getEntityManager().createQuery(jpql, getType())
                    .setParameter("value", value)
                    .setFirstResult((int) pageable.getOffset())
                    .setMaxResults(pageable.getPageSize())
                    .getResultList();

            return new PageImpl<>(content, pageable, total);
        } catch (Exception e) {
            logger.error("Error finding {} by field {} paged: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction) {
        return findByFieldSorted(fieldName, value, buildSort(sortBy, direction));
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction) {
        Pageable pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return findByFieldPaged(fieldName, value, pageable);
    }

    // ──────────── Specification Search Methods ────────────

    @Override
    public List<Entity> searchBySpecification(String search) {
        logger.info("Searching {} by Specification query: {}", getType().getSimpleName(), search);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        return (spec == null) ? getAll() : findAll(spec);
    }

    @Override
    public List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching {} by spec sorted: search={}, sort={} {}", getType().getSimpleName(), search, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        Sort sort = buildSort(sortBy, direction);
        return (spec == null) ? findAllSorted(sortBy, direction) : findAll(spec, sort);
    }

    @Override
    public Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching {} by spec paged: search={}, page={}, size={}, sort={} {}", getType().getSimpleName(), search, page, size, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        PageRequest pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return (spec == null) ? getAll(pageable) : findAll(spec, pageable);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec, Sort sort) {
        return super.findAll(spec, sort);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec) {
        return super.findAll(spec);
    }

    @Override
    public Page<Entity> findAll(Specification<Entity> spec, Pageable pageable) {
        return super.findAll(spec, pageable);
    }

    @Override
    public Page<Entity> getAll(Pageable pageable) {
        return findAll(pageable);
    }

    @Override
    public List<Entity> getAll(Sort sort) {
        return findAll(sort);
    }

    // ──────────── Helper Methods ────────────

    protected Sort buildSort(String sortBy, String direction) {
        if (sortBy == null || sortBy.isBlank() || !isValidIdentifier(sortBy)) {
            return Sort.unsorted();
        }
        return "desc".equalsIgnoreCase(direction)
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
    }

    protected String buildOrderClause(Sort sort) {
        return buildOrderClause("e", sort);
    }

    protected String buildOrderClause(String alias, Sort sort) {
        if (sort == null || sort.isUnsorted()) {
            return "";
        }
        String prefix = (alias != null && !alias.isBlank()) ? alias + "." : "";
        StringBuilder sb = new StringBuilder(" ORDER BY ");
        boolean hasOrder = false;
        for (Sort.Order order : sort) {
            if (isValidIdentifier(order.getProperty())) {
                sb.append(prefix)
                        .append(order.getProperty())
                        .append(" ")
                        .append(order.getDirection().name())
                        .append(", ");
                hasOrder = true;
            }
        }
        return hasOrder ? sb.substring(0, sb.length() - 2) : "";
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/AuthRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.auth.AuthResponse;
import com.mkii.coursemanagementsystem.dto.auth.LoginRequest;
import com.mkii.coursemanagementsystem.dto.auth.RegisterRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/api/auth")
public interface AuthRest {

    @PostMapping("/login")
    ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request);

    @PostMapping("/register")
    ResponseEntity<AuthResponse> register(@RequestBody RegisterRequest request);

    @GetMapping("/me")
    ResponseEntity<AuthResponse> getCurrentUser(Authentication authentication);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/CourseRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface CourseRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Course> createCourse(@jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Course> updateCourse(@PathVariable Long id, @jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteCourse(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<CourseResponseDTO> getCourseById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<CourseResponseDTO>> getAllCourses();

    @GetMapping(value = {"/title/{title}", "/by-title"})
    ResponseEntity<CourseResponseDTO> getCourseByTitle(
            @PathVariable(required = false) String title,
            @RequestParam(name = "queryTitle", required = false) String queryTitle,
            @RequestParam(name = "title", required = false) String paramTitle);

    @PostMapping("/batch")
    ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(@RequestBody List<CourseRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<CourseResponseDTO> getCourseByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<CourseResponseDTO>> searchCourses(@RequestParam String keyword);

    @GetMapping("/filter")
    ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(
            @RequestParam Double minPrice,
            @RequestParam Double maxPrice);

    @GetMapping("/spec-search")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/courses/sorted?sortBy=title&direction=asc
     * Returns all courses sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/paged?page=0&size=10&sortBy=price&direction=desc
     * Returns a page of courses with metadata (totalElements, totalPages, …).
     */
    @GetMapping("/paged")
    ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-sorted?search=price>100&sortBy=price&direction=asc
     * Specification filter + sort, returns flat list.
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-paged?search=price>100&page=0&size=5&sortBy=price&direction=asc
     * Specification filter + pagination + sort.
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getCourseCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/DepartmentRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/api/departments")
public interface DepartmentRest {

    @PostMapping
    ResponseEntity<DepartmentResponseDTO> create(@RequestBody DepartmentRequestDTO dto);

    @PutMapping("/{id}")
    ResponseEntity<DepartmentResponseDTO> update(@PathVariable("id") Long id, @RequestBody DepartmentRequestDTO dto);

    @DeleteMapping("/{id}")
    ResponseEntity<Void> delete(@PathVariable("id") Long id);

    @GetMapping("/{id}")
    ResponseEntity<DepartmentResponseDTO> getById(@PathVariable("id") Long id);

    @GetMapping("/code/{code}")
    ResponseEntity<DepartmentResponseDTO> getByCode(@PathVariable("code") String code);

    @GetMapping
    ResponseEntity<List<DepartmentResponseDTO>> getAll();

    @GetMapping("/search")
    ResponseEntity<List<DepartmentResponseDTO>> search(@RequestParam("keyword") String keyword);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/DocumentRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentRest {

    @PostMapping(value = {"/create", "/upload", ""}, consumes = "multipart/form-data")
    ResponseEntity<List<Document>> createDocument(
            @RequestParam("files") List<MultipartFile> files,
            @RequestParam("appId") String appId);

    @GetMapping("/download")
    ResponseEntity<byte[]> downloadDocumentByPath(@RequestParam("filePath") String filePath);

    @GetMapping("/download/{id}")
    ResponseEntity<byte[]> downloadDocumentById(@PathVariable String id);

    @PostMapping("/delete")
    ResponseEntity<String> deleteDocument(@RequestBody Map<String, String> id);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteDocumentById(@PathVariable String id);

    @GetMapping("/{id}")
    ResponseEntity<Document> getDocumentById(@PathVariable String id);

    @GetMapping("/app/{appId}")
    ResponseEntity<List<Document>> getDocumentsByAppId(@PathVariable String appId);

    @GetMapping("/app/{appId}/paged")
    ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(
            @PathVariable String appId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping(value = {"/list", ""})
    ResponseEntity<List<Document>> getAllActiveDocuments(@RequestParam(name = "appId", required = false) String appId);

    @GetMapping("/paged")
    ResponseEntity<Page<Document>> getDocumentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/sorted")
    ResponseEntity<List<Document>> getDocumentsSorted(
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<Document>> searchDocuments(
            @RequestParam(required = false) String query,
            @RequestParam(required = false, defaultValue = "0") Integer lowerLimit,
            @RequestParam(required = false, defaultValue = "10") Integer upperLimit,
            @RequestParam(required = false, defaultValue = "creationTime") String orderBy,
            @RequestParam(required = false, defaultValue = "desc") String orderType,
            @RequestParam(required = false) String appId);

    @GetMapping("/count")
    ResponseEntity<Integer> getDocCount(
            @RequestParam(required = false) String query,
            @RequestParam(required = false) String appId);

    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<Document>> searchBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/SecurityRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import io.swagger.annotations.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Api(tags = {"SecurityRest"})
@SwaggerDefinition(tags = {@Tag(name = "SecurityRest", description = "REST APIs for AES Encryption and Decryption")})
public interface SecurityRest {

    @PostMapping("/encrypt")
    @ApiOperation(value = "Encrypt plaintext payload with AES", tags = {"encrypt"}, authorizations = {
            @Authorization(value = "default", scopes = {
                    @AuthorizationScope(scope = "ROLE_ADMIN", description = "Admin role"),
                    @AuthorizationScope(scope = "ROLE_LECTURER", description = "Lecturer role")
            })
    })
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Success|OK", response = EncryptResponseDTO.class),
            @ApiResponse(code = 400, message = "Bad Request"),
            @ApiResponse(code = 403, message = "Access is denied")
    })
    @PreAuthorize("hasRole('ADMIN') or hasRole('TEACHER') or hasRole('LECTURER')")
    ResponseEntity<EncryptResponseDTO> encrypt(@Valid @RequestBody EncryptRequestDTO request);

    @PostMapping("/decrypt")
    @ApiOperation(value = "Decrypt ciphertext payload with AES", tags = {"decrypt"}, authorizations = {
            @Authorization(value = "default", scopes = {
                    @AuthorizationScope(scope = "ROLE_ADMIN", description = "Admin role"),
                    @AuthorizationScope(scope = "ROLE_TEACHER", description = "Teacher role"),
                    @AuthorizationScope(scope = "ROLE_LECTURER", description = "Lecturer role")
            })
    })
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Success|OK", response = DecryptResponseDTO.class),
            @ApiResponse(code = 400, message = "Bad Request"),
            @ApiResponse(code = 403, message = "Access is denied")
    })
    @PreAuthorize("hasRole('ADMIN') or hasRole('TEACHER') or hasRole('LECTURER')")
    ResponseEntity<DecryptResponseDTO> decrypt(@Valid @RequestBody DecryptRequestDTO request);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/StudentRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface StudentRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Student> createStudent(@jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Student> updateStudent(@PathVariable Long id, @jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteStudent(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<StudentResponseDTO> getStudentById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<StudentResponseDTO>> getAllStudents();

    @GetMapping(value = {"/email/{email}", "/by-email"})
    ResponseEntity<StudentResponseDTO> getStudentByEmail(
            @PathVariable(required = false) String email,
            @RequestParam(name = "queryEmail", required = false) String queryEmail,
            @RequestParam(name = "email", required = false) String paramEmail);

    @PostMapping("/batch")
    ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(@RequestBody List<StudentRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<StudentResponseDTO> getStudentByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<StudentResponseDTO>> searchStudents(
            @RequestParam(name = "keyword", required = false) String keyword,
            @RequestParam(name = "name", required = false) String name);

    @GetMapping("/spec-search")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/students/sorted?sortBy=fullName&direction=asc
     * Returns all students sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/paged?page=0&size=10&sortBy=fullName&direction=asc
     * Returns a page of students with metadata.
     */
    @GetMapping("/paged")
    ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-sorted?search=email:test@&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-paged?search=email:test@&page=0&size=5&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getStudentCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/AuthRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.dto.auth.AuthResponse;
import com.mkii.coursemanagementsystem.dto.auth.LoginRequest;
import com.mkii.coursemanagementsystem.dto.auth.RegisterRequest;
import com.mkii.coursemanagementsystem.entity.User;
import com.mkii.coursemanagementsystem.rest.AuthRest;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthRestImpl implements AuthRest {

    private static final Logger logger = LoggerFactory.getLogger(AuthRestImpl.class);

    private final AuthenticationManager authenticationManager;
    private final IUserDao userDao;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider tokenProvider;

    public AuthRestImpl(AuthenticationManager authenticationManager,
                        IUserDao userDao,
                        PasswordEncoder passwordEncoder,
                        JwtTokenProvider tokenProvider) {
        this.authenticationManager = authenticationManager;
        this.userDao = userDao;
        this.passwordEncoder = passwordEncoder;
        this.tokenProvider = tokenProvider;
    }

    @Override
    public ResponseEntity<AuthResponse> login(@Valid LoginRequest request) {
        logger.info("Attempting login for user: {}", request.getUsername());

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        User user = userDao.findByUsername(request.getUsername())
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + request.getUsername()));

        AuthResponse response = AuthResponse.builder()
                .token(jwt)
                .userId(user.getUserId())
                .username(user.getUsername())
                .email(user.getEmail())
                .fullName(user.getFullName())
                .role(user.getRole())
                .build();

        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<AuthResponse> register(@Valid RegisterRequest request) {
        logger.info("Registering new user: {}", request.getUsername());

        if (userDao.existsByUsername(request.getUsername())) {
            throw new BadRequestException("Username đã tồn tại: " + request.getUsername());
        }

        if (request.getEmail() != null && userDao.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email đã tồn tại: " + request.getEmail());
        }

        // Quyền mặc định khi tự đăng ký luôn là USER để ngăn chặn leo thang đặc quyền (A2)
        String role = "USER";

        User user = User.builder()
                .username(request.getUsername().trim())
                .password(passwordEncoder.encode(request.getPassword()))
                .email(request.getEmail())
                .fullName(request.getFullName())
                .role(role)
                .build();

        User savedUser = userDao.save(user);

        // Auto login after registration
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        AuthResponse response = AuthResponse.builder()
                .token(jwt)
                .userId(savedUser.getUserId())
                .username(savedUser.getUsername())
                .email(savedUser.getEmail())
                .fullName(savedUser.getFullName())
                .role(savedUser.getRole())
                .build();

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @Override
    public ResponseEntity<AuthResponse> getCurrentUser(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated() 
                || authentication instanceof org.springframework.security.authentication.AnonymousAuthenticationToken) {
            throw new org.springframework.security.authentication.InsufficientAuthenticationException("Vui lòng đăng nhập để thực hiện thao tác");
        }

        String username = authentication.getName();
        User user = userDao.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));

        AuthResponse response = AuthResponse.builder()
                .userId(user.getUserId())
                .username(user.getUsername())
                .email(user.getEmail())
                .fullName(user.getFullName())
                .role(user.getRole())
                .build();

        return ResponseEntity.ok(response);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/CourseRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.rest.CourseRest;
import com.mkii.coursemanagementsystem.service.CourseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(ApiConstants.BASE_COURSE_URL)
public class CourseRestImpl implements CourseRest {

    private static final Logger logger = LoggerFactory.getLogger(CourseRestImpl.class);

    @Autowired
    private CourseService courseService;

    @Override
    public ResponseEntity<Course> createCourse(@jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Creating new Course: {}", requestDTO.getTitle());
            Course course = courseService.create(requestDTO);
            return new ResponseEntity<>(course, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Course> updateCourse(Long id, @jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Updating Course: {}", id);
            Course course = courseService.update(requestDTO, id);
            return ResponseEntity.ok(course);
        } catch (Exception e) {
            logger.error("Error updating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteCourse(Long id) {
        try {
            logger.info("Deleting Course: {}", id);
            courseService.delete(id);
            return ResponseEntity.ok("Course deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseById(Long id) {
        try {
            logger.info("Getting Course by id: {}", id);
            CourseResponseDTO responseDTO = courseService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCourses() {
        try {
            logger.info("Getting all Courses");
            List<CourseResponseDTO> list = courseService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByTitle(String title, String queryTitle, String paramTitle) {
        try {
            String searchTitle = title != null ? title : (queryTitle != null ? queryTitle : paramTitle);
            logger.info("Getting Course by title: {}", searchTitle);
            CourseResponseDTO responseDTO = courseService.getByTitle(searchTitle);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by title: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(List<CourseRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
            List<CourseResponseDTO> result = courseService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByField(String field, String value) {
        try {
            logger.info("Getting Course by field: {} = {}", field, value);
            CourseResponseDTO responseDTO = courseService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(String field, String value) {
        try {
            logger.info("Getting Course list by field: {} = {}", field, value);
            List<CourseResponseDTO> list = courseService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Course list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Course page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCourses(String keyword) {
        try {
            logger.info("Searching Courses by keyword: {}", keyword);
            List<CourseResponseDTO> list = courseService.searchByTitle(keyword);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(Double minPrice, Double maxPrice) {
        try {
            logger.info("Filtering Courses by price: {} - {}", minPrice, maxPrice);
            List<CourseResponseDTO> list = courseService.filterByPrice(minPrice, maxPrice);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error filtering Courses by price: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(String search) {
        try {
            logger.info("Searching Courses by Specification: {}", search);
            List<CourseResponseDTO> list = courseService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
            List<CourseResponseDTO> list = courseService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec sorted: {}, {} {}", search, sortBy, direction);
            List<CourseResponseDTO> list = courseService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getCourseCount() {
        try {
            logger.info("Getting Course count");
            Integer count = courseService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Course count: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/DepartmentRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import com.mkii.coursemanagementsystem.rest.DepartmentRest;
import com.mkii.coursemanagementsystem.service.DepartmentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class DepartmentRestImpl implements DepartmentRest {

    private final DepartmentService departmentService;

    public DepartmentRestImpl(DepartmentService departmentService) {
        this.departmentService = departmentService;
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> create(@Valid DepartmentRequestDTO dto) {
        DepartmentResponseDTO created = departmentService.createDepartment(dto);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> update(Long id, @Valid DepartmentRequestDTO dto) {
        DepartmentResponseDTO updated = departmentService.updateDepartment(id, dto);
        return ResponseEntity.ok(updated);
    }

    @Override
    public ResponseEntity<Void> delete(Long id) {
        departmentService.deleteDepartment(id);
        return ResponseEntity.noContent().build();
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> getById(Long id) {
        return ResponseEntity.ok(departmentService.getDepartmentById(id));
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> getByCode(String code) {
        return ResponseEntity.ok(departmentService.getDepartmentByCode(code));
    }

    @Override
    public ResponseEntity<List<DepartmentResponseDTO>> getAll() {
        return ResponseEntity.ok(departmentService.getAllDepartments());
    }

    @Override
    public ResponseEntity<List<DepartmentResponseDTO>> search(String keyword) {
        return ResponseEntity.ok(departmentService.searchDepartments(keyword));
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/DocumentRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.rest.DocumentRest;
import com.mkii.coursemanagementsystem.service.DocumentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(ApiConstants.BASE_DOCUMENT_URL)
public class DocumentRestImpl implements DocumentRest {

    private static final Logger logger = LoggerFactory.getLogger(DocumentRestImpl.class);

    @Autowired
    private DocumentService documentService;

    @Override
    public ResponseEntity<List<Document>> createDocument(List<MultipartFile> files, String appId) {
        try {
            logger.info("REST: Creating documents for appId: {}, total files: {}", appId, files != null ? files.size() : 0);
            List<Document> documents = documentService.create(files, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error creating documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentByPath(String filePath) {
        try {
            logger.info("REST: Downloading document by filePath: {}", filePath);
            return documentService.download(filePath);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by path: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentById(String id) {
        try {
            logger.info("REST: Downloading document by id: {}", id);
            return documentService.downloadById(id);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocument(Map<String, String> id) {
        try {
            logger.info("REST: Deleting document with request body: {}", id);
            String result = documentService.delete(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocumentById(String id) {
        try {
            logger.info("REST: Deleting document by id: {}", id);
            String result = documentService.deleteById(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Document> getDocumentById(String id) {
        try {
            logger.info("REST: Getting document by id: {}", id);
            Document document = documentService.getById(id);
            return ResponseEntity.ok(document);
        } catch (Exception e) {
            logger.error("REST: Error getting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsByAppId(String appId) {
        try {
            logger.info("REST: Getting documents for appId: {}", appId);
            List<Document> documents = documentService.getByAppId(appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents for appId: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents for appId: {} paged: page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
            Page<Document> documents = documentService.getByAppIdPaged(appId, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents by appId paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getAllActiveDocuments(String appId) {
        try {
            logger.info("REST: Getting documents, appId={}", appId);
            List<Document> documents = (appId != null && !appId.isBlank())
                    ? documentService.getByAppId(appId.trim())
                    : documentService.getAllActive();
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<Document> documents = documentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsSorted(String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents sorted: sort={} {}", sortBy, direction);
            List<Document> documents = documentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> searchDocuments(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        try {
            logger.info("REST: Searching documents: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                    query, lowerLimit, upperLimit, orderBy, orderType, appId);
            List<Document> documents = documentService.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getDocCount(String query, String appId) {
        try {
            logger.info("REST: Getting document count: query={}, appId={}", query, appId);
            Integer count = documentService.getDocCount(query, appId);
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("REST: Error getting document count: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Searching documents by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<Document> documents = documentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents by spec paged: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/SecurityRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.rest.SecurityRest;
import com.mkii.coursemanagementsystem.service.SecurityService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(ApiConstants.BASE_SECURITY_URL)
public class SecurityRestImpl implements SecurityRest {

    private static final Logger logger = LoggerFactory.getLogger(SecurityRestImpl.class);

    private final SecurityService securityService;

    public SecurityRestImpl(SecurityService securityService) {
        this.securityService = securityService;
    }

    @Override
    public ResponseEntity<EncryptResponseDTO> encrypt(@Valid EncryptRequestDTO request) {
        try {
            logger.info("REST: Encrypting request payload");
            EncryptResponseDTO response = securityService.encrypt(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("REST: Error during encrypt: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<DecryptResponseDTO> decrypt(@Valid DecryptRequestDTO request) {
        try {
            logger.info("REST: Decrypting request payload");
            DecryptResponseDTO response = securityService.decrypt(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("REST: Error during decrypt: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/StudentRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.rest.StudentRest;
import com.mkii.coursemanagementsystem.service.StudentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(ApiConstants.BASE_STUDENT_URL)
public class StudentRestImpl implements StudentRest {

    private static final Logger logger = LoggerFactory.getLogger(StudentRestImpl.class);

    @Autowired
    private StudentService studentService;

    @Override
    public ResponseEntity<Student> createStudent(@jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Creating new Student: {}", requestDTO.getFullName());
            Student student = studentService.create(requestDTO);
            return new ResponseEntity<>(student, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Student> updateStudent(Long id, @jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Updating Student: {}", id);
            Student student = studentService.update(requestDTO, id);
            return ResponseEntity.ok(student);
        } catch (Exception e) {
            logger.error("Error updating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteStudent(Long id) {
        try {
            logger.info("Deleting Student: {}", id);
            studentService.delete(id);
            return ResponseEntity.ok("Student deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentById(Long id) {
        try {
            logger.info("Getting Student by id: {}", id);
            StudentResponseDTO responseDTO = studentService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudents() {
        try {
            logger.info("Getting all Students");
            List<StudentResponseDTO> list = studentService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByEmail(String email, String queryEmail, String paramEmail) {
        try {
            String searchEmail = email != null ? email : (queryEmail != null ? queryEmail : paramEmail);
            logger.info("Getting Student by email: {}", searchEmail);
            StudentResponseDTO responseDTO = studentService.getByEmail(searchEmail);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by email: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(List<StudentRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Students", requestDTOs != null ? requestDTOs.size() : 0);
            List<StudentResponseDTO> result = studentService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByField(String field, String value) {
        try {
            logger.info("Getting Student by field: {} = {}", field, value);
            StudentResponseDTO responseDTO = studentService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(String field, String value) {
        try {
            logger.info("Getting Student list by field: {} = {}", field, value);
            List<StudentResponseDTO> list = studentService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Student list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Student page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudents(String keyword, String name) {
        String searchKey = (keyword != null && !keyword.isBlank()) ? keyword : name;
        if (searchKey == null) {
            searchKey = "";
        }
        try {
            logger.info("Searching Students by keyword: {}", searchKey);
            List<StudentResponseDTO> list = studentService.searchByKeyword(searchKey);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(String search) {
        try {
            logger.info("Searching Students by Specification: {}", search);
            List<StudentResponseDTO> list = studentService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Students sorted by {} {}", sortBy, direction);
            List<StudentResponseDTO> list = studentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec sorted: {}, {} {}", search, sortBy, direction);
            List<StudentResponseDTO> list = studentService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Students by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getStudentCount() {
        try {
            logger.info("Getting Student count");
            Integer count = studentService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Student count: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/security/jwt/JwtAccessDeniedHandler.java`

```java
package com.mkii.coursemanagementsystem.security.jwt;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.MediaType;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Component
public class JwtAccessDeniedHandler implements AccessDeniedHandler {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response,
                       AccessDeniedException accessDeniedException) throws IOException, ServletException {
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setStatus(HttpServletResponse.SC_FORBIDDEN);

        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        body.put("status", HttpServletResponse.SC_FORBIDDEN);
        body.put("error", "Forbidden");
        body.put("message", "Tài khoản của bạn không có quyền hạn truy cập tài nguyên này!");
        body.put("path", request.getServletPath());

        objectMapper.writeValue(response.getOutputStream(), body);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/security/jwt/JwtAuthenticationEntryPoint.java`

```java
package com.mkii.coursemanagementsystem.security.jwt;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.MediaType;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Component
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response,
                         AuthenticationException authException) throws IOException, ServletException {
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);

        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        body.put("status", HttpServletResponse.SC_UNAUTHORIZED);
        body.put("error", "Unauthorized");
        body.put("message", "Bạn cần đăng nhập (truyền Bearer Token) để thực hiện thao tác này!");
        body.put("path", request.getServletPath());

        objectMapper.writeValue(response.getOutputStream(), body);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/security/jwt/JwtAuthenticationFilter.java`

```java
package com.mkii.coursemanagementsystem.security.jwt;

import com.mkii.coursemanagementsystem.security.service.UserDetailsServiceImpl;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtTokenProvider tokenProvider;
    private final UserDetailsServiceImpl userDetailsService;

    public JwtAuthenticationFilter(JwtTokenProvider tokenProvider, UserDetailsServiceImpl userDetailsService) {
        this.tokenProvider = tokenProvider;
        this.userDetailsService = userDetailsService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        try {
            String jwt = parseJwt(request);
            if (StringUtils.hasText(jwt) && tokenProvider.validateToken(jwt)) {
                String username = tokenProvider.getUsernameFromToken(jwt);

                UserDetails userDetails = userDetailsService.loadUserByUsername(username);
                UsernamePasswordAuthenticationToken authentication =
                        new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception e) {
            logger.error("Không thể thiết lập xác thực người dùng trong Security Context: {}", e.getMessage());
        }

        filterChain.doFilter(request, response);
    }

    private String parseJwt(HttpServletRequest request) {
        String headerAuth = request.getHeader("Authorization");
        if (StringUtils.hasText(headerAuth) && headerAuth.startsWith("Bearer ")) {
            return headerAuth.substring(7);
        }
        return null;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/security/jwt/JwtTokenProvider.java`

```java
package com.mkii.coursemanagementsystem.security.jwt;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.stream.Collectors;

@Component
public class JwtTokenProvider {

    private static final Logger logger = LoggerFactory.getLogger(JwtTokenProvider.class);

    @Value("${jwt.secret:9a4f2c8d3b7a1e6f4c8b2d0e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a}")
    private String jwtSecret;

    @Value("${jwt.expiration:86400000}")
    private long jwtExpirationMs;

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }

    public String generateToken(Authentication authentication) {
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        String roles = userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(","));

        return generateTokenFromUsername(userDetails.getUsername(), roles);
    }

    public String generateTokenFromUsername(String username, String role) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + jwtExpirationMs);

        return Jwts.builder()
                .subject(username)
                .claim("role", role)
                .issuedAt(now)
                .expiration(expiryDate)
                .signWith(getSigningKey())
                .compact();
    }

    public String getUsernameFromToken(String token) {
        Claims claims = Jwts.parser()
                .verifyWith(getSigningKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();

        return claims.getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                    .verifyWith(getSigningKey())
                    .build()
                    .parseSignedClaims(token);
            return true;
        } catch (SecurityException | MalformedJwtException e) {
            logger.error("Chữ ký JWT không hợp lệ: {}", e.getMessage());
        } catch (ExpiredJwtException e) {
            logger.error("Token JWT đã hết hạn: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            logger.error("Token JWT không được hỗ trợ: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            logger.error("Chuỗi JWT claims rỗng: {}", e.getMessage());
        }
        return false;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/security/service/UserDetailsServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.security.service;

import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.entity.User;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.List;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    private final IUserDao userDao;

    public UserDetailsServiceImpl(@Lazy IUserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userDao.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("Không tìm thấy người dùng với username: " + username));

        String role = user.getRole();
        if (role == null || role.trim().isEmpty()) {
            role = "USER";
        }
        if (!role.startsWith("ROLE_")) {
            role = "ROLE_" + role;
        }

        List<SimpleGrantedAuthority> authorities = Collections.singletonList(new SimpleGrantedAuthority(role));

        return new org.springframework.security.core.userdetails.User(
                user.getUsername(),
                user.getPassword(),
                authorities
        );
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/CourseService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;

import java.util.List;

public interface CourseService {

    Course create(CourseRequestDTO requestDTO);

    Course update(CourseRequestDTO requestDTO, Long id);

    void delete(Long id);

    CourseResponseDTO getById(Long id);

    List<CourseResponseDTO> getAll();

    List<CourseResponseDTO> searchByTitle(String keyword);

    List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice);

    CourseResponseDTO getByTitle(String title);

    CourseResponseDTO getByField(String field, Object value);

    /** Find multiple courses matching a specific field value (returns list). */
    List<CourseResponseDTO> findByFieldList(String field, Object value);

    /** Find courses matching a field with pagination and sorting. */
    Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple courses at once. */
    List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs);

    List<CourseResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all courses sorted by a field ("title", "price", …) and direction ("asc"/"desc"). */
    List<CourseResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of courses, sorted. */
    Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/DepartmentService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;

import java.util.List;

public interface DepartmentService {

    DepartmentResponseDTO createDepartment(DepartmentRequestDTO dto);

    DepartmentResponseDTO updateDepartment(Long id, DepartmentRequestDTO dto);

    void deleteDepartment(Long id);

    DepartmentResponseDTO getDepartmentById(Long id);

    DepartmentResponseDTO getDepartmentByCode(String code);

    List<DepartmentResponseDTO> getAllDepartments();

    List<DepartmentResponseDTO> searchDepartments(String keyword);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/DocumentService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentService {

    List<Document> create(List<MultipartFile> files, String appId);

    Document createDocument(String fileName, String appId, String fileobj);

    Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail);

    ResponseEntity<byte[]> download(String filePath);

    ResponseEntity<byte[]> downloadById(String id);

    String delete(Map<String, String> id);

    String deleteById(String id);

    Document fetchAndValidateDocumentById(Map<String, String> id);

    Document getById(String id);

    List<Document> getByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> getAllPaged(int page, int size, String sortBy, String direction);

    List<Document> getAllSorted(String sortBy, String direction);

    Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction);

    Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/MinioStorageService.java`

```java
package com.mkii.coursemanagementsystem.service;

import io.minio.BucketExistsArgs;
import io.minio.GetObjectArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.InputStream;

@Service
public class MinioStorageService {

    private static final Logger logger = LoggerFactory.getLogger(MinioStorageService.class);

    @Autowired
    private MinioClient minioClient;

    @Value("${minio.bucket-name:documents}")
    private String bucketName;

    public void ensureBucketExists() {
        try {
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
            if (!exists) {
                logger.info("MinIO bucket '{}' does not exist. Creating bucket...", bucketName);
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
            }
        } catch (Exception e) {
            logger.error("Error verifying/creating MinIO bucket '{}': {}", bucketName, e.getMessage());
            throw new RuntimeException("Could not connect to MinIO storage: " + e.getMessage(), e);
        }
    }

    public void upload(String objectPath, InputStream inputStream, String contentType, long size) {
        ensureBucketExists();
        try {
            logger.info("Uploading object '{}' to MinIO bucket '{}' (size: {} bytes)", objectPath, bucketName, size);
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .stream(inputStream, size, -1)
                            .contentType(contentType != null ? contentType : "application/octet-stream")
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error uploading object '{}' to MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to upload file to MinIO: " + e.getMessage(), e);
        }
    }

    public byte[] download(String objectPath) {
        try {
            logger.info("Downloading object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            try (InputStream stream = minioClient.getObject(
                    GetObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build())) {
                return IOUtils.toByteArray(stream);
            }
        } catch (Exception e) {
            logger.error("Error downloading object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to download file from MinIO: " + e.getMessage(), e);
        }
    }

    public void delete(String objectPath) {
        try {
            logger.info("Removing object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            minioClient.removeObject(
                    RemoveObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error deleting object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to delete file from MinIO: " + e.getMessage(), e);
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/SecurityService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;

public interface SecurityService {

    /**
     * Encrypts plaintext string using AES CBC mode with random IV.
     */
    EncryptResponseDTO encrypt(EncryptRequestDTO request);

    /**
     * Decrypts Base64 ciphertext with prepended IV back to original plaintext.
     */
    DecryptResponseDTO decrypt(DecryptRequestDTO request);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/StudentService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;

import java.util.List;

public interface StudentService {

    Student create(StudentRequestDTO requestDTO);

    Student update(StudentRequestDTO requestDTO, Long id);

    void delete(Long id);

    StudentResponseDTO getById(Long id);

    List<StudentResponseDTO> getAll();

    List<StudentResponseDTO> searchByKeyword(String keyword);

    StudentResponseDTO getByEmail(String email);

    StudentResponseDTO getByField(String field, Object value);

    /** Find multiple students matching a specific field value (returns list). */
    List<StudentResponseDTO> findByFieldList(String field, Object value);

    /** Find students matching a field with pagination and sorting. */
    Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple students at once. */
    List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs);

    List<StudentResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all students sorted by a field ("fullName", "email", …) and direction ("asc"/"desc"). */
    List<StudentResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of students, sorted. */
    Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/CourseServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.service.CourseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class CourseServiceImpl implements CourseService {

    private static final Logger logger = LoggerFactory.getLogger(CourseServiceImpl.class);

    // Call ONLY ICourseDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private ICourseDao courseDao;

    @Override
    public Course create(CourseRequestDTO requestDTO) {
        logger.info("Creating Course: {}", requestDTO.getTitle());
        Course course = new Course();
        mapRequestToEntity(requestDTO, course);
        return courseDao.save(course);
    }

    @Override
    public Course update(CourseRequestDTO requestDTO, Long id) {
        logger.info("Updating Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        mapRequestToEntity(requestDTO, existing);
        return courseDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        courseDao.delete(id);
    }

    @Override
    public CourseResponseDTO getById(Long id) {
        logger.info("Getting Course by id: {}", id);
        Course course = courseDao.getById(id);
        if (course == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> getAll() {
        logger.info("Getting all Courses");
        return courseDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> searchByTitle(String keyword) {
        logger.info("Searching Courses by title: {}", keyword);
        return courseDao.searchByTitle(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice) {
        logger.info("Filtering Courses by price range: {} - {}", minPrice, maxPrice);
        return courseDao.findByPriceRange(minPrice, maxPrice)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public CourseResponseDTO getByTitle(String title) {
        logger.info("Getting Course by title: {}", title);
        Course course = courseDao.getByTitle(title);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với tiêu đề: " + title);
        }
        return mapToDTO(course);
    }

    @Override
    public CourseResponseDTO getByField(String field, Object value) {
        logger.info("Getting Course by field: {} = {}", field, value);
        Course course = courseDao.getByField(field, value);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với " + field + ": " + value);
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Course list by field: {} = {}", field, value);
        return courseDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return courseDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Course> entities = requestDTOs.stream().map(dto -> {
            Course course = new Course();
            mapRequestToEntity(dto, course);
            return course;
        }).collect(Collectors.toList());
        return courseDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to ICourseDao) ────────────

    @Override
    public List<CourseResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Courses by Specification query: {}", search);
        return courseDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
        return courseDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return courseDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Courses by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return courseDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Courses by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return courseDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Course count");
        return courseDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(CourseRequestDTO requestDTO, Course course) {
        if (requestDTO.getTitle() != null) {
            course.setTitle(requestDTO.getTitle());
        }
        if (requestDTO.getDescription() != null) {
            course.setDescription(requestDTO.getDescription());
        }
        if (requestDTO.getDuration() != null) {
            course.setDuration(requestDTO.getDuration());
        }
        if (requestDTO.getPrice() != null) {
            course.setPrice(requestDTO.getPrice());
        }
    }

    private CourseResponseDTO mapToDTO(Course course) {
        return new CourseResponseDTO(
                course.getId(),
                course.getTitle(),
                course.getDescription(),
                course.getDuration(),
                course.getPrice()
        );
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/DepartmentServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.service.DepartmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class DepartmentServiceImpl implements DepartmentService {

    private static final Logger logger = LoggerFactory.getLogger(DepartmentServiceImpl.class);

    private final IDepartmentDao departmentDao;

    public DepartmentServiceImpl(IDepartmentDao departmentDao) {
        this.departmentDao = departmentDao;
    }

    @Override
    public DepartmentResponseDTO createDepartment(DepartmentRequestDTO dto) {
        if (dto.getDepartmentCode() == null || dto.getDepartmentCode().trim().isEmpty()) {
            throw new BadRequestException("Mã khoa không được để trống.");
        }
        String normalizedCode = dto.getDepartmentCode().trim().toUpperCase();
        logger.info("Creating Department with code: {}", normalizedCode);
        if (departmentDao.findByDepartmentCode(normalizedCode).isPresent()) {
            throw new BadRequestException("Mã khoa đã tồn tại: " + normalizedCode);
        }

        Department department = Department.builder()
                .departmentCode(normalizedCode)
                .departmentName(dto.getDepartmentName() != null ? dto.getDepartmentName().trim() : "")
                .description(dto.getDescription())
                .build();

        Department saved = departmentDao.save(department);
        return toDTO(saved);
    }

    @Override
    public DepartmentResponseDTO updateDepartment(Long id, DepartmentRequestDTO dto) {
        logger.info("Updating Department with ID: {}", id);
        Department existing = departmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }

        if (dto.getDepartmentCode() != null && !dto.getDepartmentCode().trim().isEmpty()) {
            String normalizedCode = dto.getDepartmentCode().trim().toUpperCase();
            departmentDao.findByDepartmentCode(normalizedCode).ifPresent(d -> {
                if (!d.getDepartmentId().equals(id)) {
                    throw new BadRequestException("Mã khoa đã tồn tại: " + normalizedCode);
                }
            });
            existing.setDepartmentCode(normalizedCode);
        }

        if (dto.getDepartmentName() != null) {
            existing.setDepartmentName(dto.getDepartmentName().trim());
        }
        existing.setDescription(dto.getDescription());

        Department updated = departmentDao.update(existing);
        return toDTO(updated);
    }

    @Override
    public void deleteDepartment(Long id) {
        logger.info("Deleting Department with ID: {}", id);
        Department existing = departmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }
        departmentDao.delete(id);
    }

    @Override
    @Transactional(readOnly = true)
    public DepartmentResponseDTO getDepartmentById(Long id) {
        Department department = departmentDao.getById(id);
        if (department == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }
        return toDTO(department);
    }

    @Override
    @Transactional(readOnly = true)
    public DepartmentResponseDTO getDepartmentByCode(String code) {
        return departmentDao.findByDepartmentCode(code)
                .map(this::toDTO)
                .orElseThrow(() -> new ResourceNotFoundException("Department not found with code: " + code));
    }

    @Override
    @Transactional(readOnly = true)
    public List<DepartmentResponseDTO> getAllDepartments() {
        return departmentDao.getAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<DepartmentResponseDTO> searchDepartments(String keyword) {
        return departmentDao.searchByName(keyword).stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private DepartmentResponseDTO toDTO(Department d) {
        return DepartmentResponseDTO.builder()
                .departmentId(d.getDepartmentId())
                .departmentCode(d.getDepartmentCode())
                .departmentName(d.getDepartmentName())
                .description(d.getDescription())
                .createdAt(d.getCreatedAt())
                .updatedAt(d.getUpdatedAt())
                .build();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/DocumentServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.service.DocumentService;
import com.mkii.coursemanagementsystem.service.MinioStorageService;
import org.apache.commons.io.FilenameUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
@Transactional
public class DocumentServiceImpl implements DocumentService {

    private static final Logger logger = LoggerFactory.getLogger(DocumentServiceImpl.class);

    private static final String[] SUPPORTED_EXTENSIONS = {
            "pdf", "xlsx", "xls", "doc", "docx", "jpg", "jpeg", "png"
    };

    // Strict architectural compliance: call ONLY IDocumentDao interface
    @Autowired
    private IDocumentDao documentDao;

    @Autowired
    private MinioStorageService minioStorageService;

    @Override
    @Transactional
    public List<Document> create(List<MultipartFile> files, String appId) {
        logger.info("Starting document creation for appId: {}, total files: {}", appId, files != null ? files.size() : 0);

        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId (mã công việc/nghiệp vụ) không được để trống.");
        }
        if (files == null || files.isEmpty()) {
            throw new BadRequestException("Danh sách file tải lên không hợp lệ hoặc để trống.");
        }

        List<Document> documentList = new ArrayList<>();
        List<String> uploadedStoragePaths = new ArrayList<>();

        try {
            for (MultipartFile file : files) {
                if (file != null && !file.isEmpty() && file.getOriginalFilename() != null && !file.getOriginalFilename().trim().isEmpty()) {
                    String originalFilename = FilenameUtils.getName(file.getOriginalFilename());

                    // 1. Kiểm tra ký tự đặc biệt trong tên file
                    if (!checkFileNameSpecialChar(originalFilename)) {
                        throw new BadRequestException("Tên file không được chứa ký tự đặc biệt: " + originalFilename);
                    }

                    // 2. Kiểm tra độ dài tên file (phần trước dấu chấm <= 50 ký tự)
                    String baseName = FilenameUtils.getBaseName(originalFilename);
                    if (baseName.length() > 50) {
                        throw new BadRequestException("Tên file vượt quá độ dài tối đa 50 ký tự: " + baseName);
                    }

                    // 3. Kiểm tra định dạng đuôi file
                    String extension = FilenameUtils.getExtension(originalFilename);
                    String storagePath = appId + "/" + UUID.randomUUID() + (extension.isEmpty() ? "" : "." + extension);

                    try (InputStream inputStream = validateFileExtension(file)) {
                        // 4. Lưu trữ file lên MinIO
                        minioStorageService.upload(storagePath, inputStream, file.getContentType(), file.getSize());
                        uploadedStoragePaths.add(storagePath);
                    }

                    // 5. Kiểm tra tài liệu cùng tên đã tồn tại cho appId này chưa (Versioning logic)
                    Document documentDetail = documentDao.getDocumentName(originalFilename, appId);
                    if (documentDetail == null) {
                        Document docData = createDocument(originalFilename, appId, storagePath);
                        documentList.add(docData);
                    } else {
                        logger.info("Tài liệu '{}' đã tồn tại, tạo phiên bản mới", documentDetail.getName());
                        Document docDataWithNewVersion = createDocumentWithNewVersion(originalFilename, appId, storagePath, documentDetail);
                        documentList.add(docDataWithNewVersion);
                    }
                } else {
                    throw new BadRequestException("File tải lên không được để trống.");
                }
            }
            return documentList;
        } catch (RuntimeException ex) {
            // Rollback bù trừ (Compensating action): xóa các file đã tải lên MinIO nếu giao dịch thất bại (A6)
            for (String path : uploadedStoragePaths) {
                try {
                    logger.warn("MinIO compensating rollback: xóa object mồ côi {}", path);
                    minioStorageService.delete(path);
                } catch (Exception cleanupEx) {
                    logger.error("Lỗi dọn dẹp file MinIO mồ côi {}: {}", path, cleanupEx.getMessage());
                }
            }
            throw ex;
        } catch (Exception ex) {
            for (String path : uploadedStoragePaths) {
                try {
                    logger.warn("MinIO compensating rollback: xóa object mồ côi {}", path);
                    minioStorageService.delete(path);
                } catch (Exception cleanupEx) {
                    logger.error("Lỗi dọn dẹp file MinIO mồ côi {}: {}", path, cleanupEx.getMessage());
                }
            }
            throw new RuntimeException("Lỗi trong quá trình upload tài liệu: " + ex.getMessage(), ex);
        }
    }

    @Override
    public Document createDocument(String fileName, String appId, String fileobj) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);
        doc.setVersion(1.0);
        return documentDao.save(doc);
    }

    @Override
    public Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);

        // Vô hiệu hóa phiên bản cũ
        if (Boolean.TRUE.equals(documentDetail.getActive())) {
            documentDetail.setActive(false);
            documentDao.update(documentDetail);
        }

        // Tăng số phiên bản cho tài liệu mới
        Double versionCount = documentDetail.getVersion() != null ? documentDetail.getVersion() : 1.0;
        doc.setVersion(++versionCount);
        return documentDao.save(doc);
    }

    private void setDocumentDetails(String fileName, String appId, String fileobj, Document doc) {
        doc.setAppId(appId);
        doc.setName(fileName);
        doc.setPath(fileobj);
        doc.setOwner("SYSTEM");
        doc.setDeleted(false);
        doc.setActive(true);
    }

    public static boolean checkFileNameSpecialChar(String fileName) {
        if (fileName == null || fileName.isBlank()) {
            return false;
        }
        return fileName.matches("^[a-zA-Z0-9._\\s\\p{L}-]+$");
    }

    @Override
    public ResponseEntity<byte[]> download(String filePath) {
        logger.info("Downloading document by filePath: {}", filePath);
        if (filePath == null || filePath.trim().isEmpty()) {
            throw new BadRequestException("Đường dẫn file không được để trống.");
        }

        byte[] data = minioStorageService.download(filePath);
        String filename = FilenameUtils.getName(filePath);
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public ResponseEntity<byte[]> downloadById(String id) {
        logger.info("Downloading document by id: {}", id);
        Document document = getById(id);
        byte[] data = minioStorageService.download(document.getPath());

        String filename = document.getName() != null ? document.getName() : FilenameUtils.getName(document.getPath());
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public String delete(Map<String, String> id) {
        Document document = fetchAndValidateDocumentById(id);
        logger.info("Soft deleting document name: {}, id: {}", document.getName(), document.getId());
        document.setDeleted(true);
        document.setActive(false);
        documentDao.update(document);
        return MessageConstants.SUCCESS_JSON;
    }

    @Override
    public String deleteById(String id) {
        return delete(Map.of("id", id));
    }

    @Override
    public Document fetchAndValidateDocumentById(Map<String, String> id) {
        if (id == null) {
            throw new BadRequestException(MessageConstants.INVALID_DOCUMENT);
        }
        String docId = id.get("id");
        if (docId == null) {
            docId = id.get("ID");
        }
        if (docId != null && !docId.trim().isEmpty()) {
            Document document = documentDao.findByPk(docId.trim());
            if (document != null && !Boolean.TRUE.equals(document.getDeleted())) {
                return document;
            }
        }
        throw new ResourceNotFoundException(MessageConstants.INVALID_DOCUMENT);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting document by id: {}", id);
        Document document = documentDao.findByPk(id);
        if (document == null || Boolean.TRUE.equals(document.getDeleted())) {
            throw new ResourceNotFoundException(String.format(MessageConstants.DOCUMENT_NOT_FOUND, id));
        }
        return document;
    }

    @Override
    public List<Document> getByAppId(String appId) {
        logger.info("Getting documents for appId: {}", appId);
        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId không được để trống.");
        }
        return documentDao.getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active documents");
        return documentDao.getAllActive();
    }

    // ──────────── Pagination, Sorting & Search (Delegated to IDocumentDao) ────────────

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("Service getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);
        return documentDao.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("Service getDocCount: query={}, appId={}", query, appId);
        return documentDao.getDocCount(query, appId);
    }

    @Override
    public Page<Document> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Service getAllPaged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return documentDao.findAllPaged(page, size, sortBy, direction);
    }

    @Override
    public List<Document> getAllSorted(String sortBy, String direction) {
        logger.info("Service getAllSorted: sort={} {}", sortBy, direction);
        return documentDao.findAllSorted(sortBy, direction);
    }

    @Override
    public Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("Service getByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        return documentDao.findByAppIdPaged(appId, page, size, sortBy, direction);
    }

    @Override
    public Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Service searchBySpecificationPaged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return documentDao.searchBySpecificationPaged(search, page, size, sortBy, direction);
    }

    // ──────────── Private helper methods ────────────

    private InputStream validateFileExtension(MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null) {
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }

        String extension = FilenameUtils.getExtension(originalFilename).toLowerCase();
        logger.info("Validating extension from multipart: '{}'", extension);

        if (Arrays.asList(SUPPORTED_EXTENSIONS).contains(extension)) {
            try {
                return file.getInputStream();
            } catch (IOException e) {
                logger.error("Error reading file input stream: {}", e.getMessage(), e);
                throw new BadRequestException("Không thể đọc dữ liệu file: " + e.getMessage());
            }
        } else {
            logger.warn("File extension '{}' is not supported", extension);
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/SecurityServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.service.SecurityService;
import com.mkii.coursemanagementsystem.util.AESUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;

@Service
public class SecurityServiceImpl implements SecurityService {

    private static final Logger logger = LoggerFactory.getLogger(SecurityServiceImpl.class);
    private static final String DEFAULT_KEY = System.getenv("CMS_AES_KEY") != null
            ? System.getenv("CMS_AES_KEY") : "CourseManagementSystemSecretKey2026";
    private static final String DEFAULT_SALT = System.getenv("CMS_AES_SALT") != null
            ? System.getenv("CMS_AES_SALT") : "cms-salt-2026-v1";

    private final SecretKey secretKey;

    public SecurityServiceImpl() {
        this(DEFAULT_KEY, DEFAULT_SALT);
    }

    @Autowired
    public SecurityServiceImpl(
            @Value("${cms.security.aes-key:" + "CourseManagementSystemSecretKey2026}") String aesKey,
            @Value("${cms.security.aes-salt:" + "cms-salt-2026-v1}") String aesSalt) {
        try {
            this.secretKey = AESUtil.getKeyFromPassword(aesKey, aesSalt);
        } catch (Exception e) {
            throw new ExceptionInInitializerError("Could not initialize SecurityService SecretKey: " + e.getMessage());
        }
    }

    @Override
    public EncryptResponseDTO encrypt(EncryptRequestDTO request) {
        if (request == null || request.getData() == null) {
            throw new BadRequestException(MessageConstants.DATA_TO_ENCRYPT_CANNOT_BE_EMPTY);
        }
        try {
            logger.info("Encrypting sensitive payload of length {}", request.getData().length());
            String encrypted = AESUtil.encryptStringWithIv(request.getData(), this.secretKey);
            return EncryptResponseDTO.builder()
                    .encryptedData(encrypted)
                    .algorithm(AESUtil.DEFAULT_ALGORITHM)
                    .build();
        } catch (Exception e) {
            logger.error("Error during encryption: {}", e.getMessage(), e);
            throw new BadRequestException(String.format(MessageConstants.ENCRYPTION_FAILED, e.getMessage()));
        }
    }

    @Override
    public DecryptResponseDTO decrypt(DecryptRequestDTO request) {
        if (request == null || request.getEncryptedData() == null) {
            throw new BadRequestException(MessageConstants.DATA_TO_DECRYPT_CANNOT_BE_EMPTY);
        }
        try {
            logger.info("Decrypting payload of length {}", request.getEncryptedData().length());
            String decrypted = AESUtil.decryptStringWithIv(request.getEncryptedData(), this.secretKey);
            return DecryptResponseDTO.builder()
                    .decryptedData(decrypted)
                    .build();
        } catch (Exception e) {
            logger.error("Error during decryption: {}", e.getMessage(), e);
            throw new BadRequestException(String.format(MessageConstants.DECRYPTION_FAILED, e.getMessage()));
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/StudentServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.StudentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class StudentServiceImpl implements StudentService {

    private static final Logger logger = LoggerFactory.getLogger(StudentServiceImpl.class);

    // Call ONLY IStudentDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private IStudentDao studentDao;

    @Autowired
    private com.mkii.coursemanagementsystem.dao.IDepartmentDao departmentDao;

    @Override
    public Student create(StudentRequestDTO requestDTO) {
        logger.info("Creating Student: {}", requestDTO.getFullName());
        if (requestDTO.getEmail() != null) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        Student student = new Student();
        mapRequestToEntity(requestDTO, student);
        return studentDao.save(student);
    }

    @Override
    public Student update(StudentRequestDTO requestDTO, Long id) {
        logger.info("Updating Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        if (requestDTO.getEmail() != null && !requestDTO.getEmail().equalsIgnoreCase(existing.getEmail())) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null && !existingByEmail.getId().equals(id)) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        mapRequestToEntity(requestDTO, existing);
        return studentDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        studentDao.delete(id);
    }

    @Override
    public StudentResponseDTO getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        Student student = studentDao.getById(id);
        if (student == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> getAll() {
        logger.info("Getting all Students");
        return studentDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return studentDao.searchByKeyword(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public StudentResponseDTO getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        Student student = studentDao.getByEmail(email);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với email: " + email);
        }
        return mapToDTO(student);
    }

    @Override
    public StudentResponseDTO getByField(String field, Object value) {
        logger.info("Getting Student by field: {} = {}", field, value);
        Student student = studentDao.getByField(field, value);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với " + field + ": " + value);
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Student list by field: {} = {}", field, value);
        return studentDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return studentDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Students", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Student> entities = requestDTOs.stream().map(dto -> {
            Student student = new Student();
            mapRequestToEntity(dto, student);
            return student;
        }).collect(Collectors.toList());
        return studentDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to IStudentDao) ────────────

    @Override
    public List<StudentResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Students by Specification query: {}", search);
        return studentDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Students sorted by {} {}", sortBy, direction);
        return studentDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return studentDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Students by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return studentDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Students by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return studentDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return studentDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(StudentRequestDTO requestDTO, Student student) {
        if (requestDTO.getFullName() != null) {
            student.setFullName(requestDTO.getFullName());
        }
        if (requestDTO.getEmail() != null) {
            student.setEmail(requestDTO.getEmail());
        }
        if (requestDTO.getPhone() != null) {
            student.setPhone(requestDTO.getPhone());
        }
        if (requestDTO.getAddress() != null) {
            student.setAddress(requestDTO.getAddress());
        }
        if (requestDTO.getDob() != null) {
            student.setDob(requestDTO.getDob());
        }
        if (requestDTO.getDepartmentId() != null) {
            com.mkii.coursemanagementsystem.entity.Department dept = departmentDao.getById(requestDTO.getDepartmentId());
            if (dept == null) {
                throw new ResourceNotFoundException("Khoa không tồn tại với ID: " + requestDTO.getDepartmentId());
            }
            student.setDepartment(dept);
        }
    }

    private StudentResponseDTO mapToDTO(Student student) {
        com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO deptDTO = null;
        if (student.getDepartment() != null) {
            deptDTO = com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO.builder()
                    .departmentId(student.getDepartment().getDepartmentId())
                    .departmentCode(student.getDepartment().getDepartmentCode())
                    .departmentName(student.getDepartment().getDepartmentName())
                    .description(student.getDepartment().getDescription())
                    .build();
        }
        return StudentResponseDTO.builder()
                .id(student.getId())
                .fullName(student.getFullName())
                .email(student.getEmail())
                .phone(student.getPhone())
                .address(student.getAddress())
                .dob(student.getDob())
                .department(deptDTO)
                .build();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/GenericSpecification.java`

```java
package com.mkii.coursemanagementsystem.specification;

import jakarta.persistence.criteria.*;
import org.springframework.data.jpa.domain.Specification;

public class GenericSpecification<T> implements Specification<T> {

    private final SearchCriteria criteria;

    public GenericSpecification(SearchCriteria criteria) {
        this.criteria = criteria;
    }

    public SearchCriteria getCriteria() {
        return criteria;
    }

    @Override
    public Predicate toPredicate(Root<T> root, CriteriaQuery<?> query, CriteriaBuilder builder) {
        if (criteria == null || criteria.getKey() == null) {
            return null;
        }

        Path<?> path;
        try {
            path = root.get(criteria.getKey());
        } catch (IllegalArgumentException e) {
            return null; // Field does not exist on entity
        }

        String operation = criteria.getOperation();
        Object value = criteria.getValue();
        if (value == null) {
            return null;
        }

        String strValue = value.toString();
        Class<?> javaType = path.getJavaType();

        switch (operation) {
            case ">":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.gt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case ">=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.ge(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.lt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.le(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "!":
            case "!=":
                if (javaType == String.class) {
                    return builder.notLike(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                }
                Object castVal = castToRequiredType(javaType, strValue);
                return castVal != null ? builder.notEqual(path, castVal) : null;

            case ":":
            default:
                if (javaType == String.class) {
                    return builder.like(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                } else {
                    Object eqVal = castToRequiredType(javaType, strValue);
                    return eqVal != null ? builder.equal(path, eqVal) : null;
                }
        }
        return null;
    }

    private Number parseNumber(Class<?> targetType, String str) {
        try {
            if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            }
            return Double.parseDouble(str);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Object castToRequiredType(Class<?> targetType, String str) {
        try {
            if (targetType == String.class) {
                return str;
            } else if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            } else if (targetType == Boolean.class || targetType == boolean.class) {
                return Boolean.parseBoolean(str);
            }
            return str;
        } catch (Exception e) {
            return null;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/GenericSpecificationsBuilder.java`

```java
package com.mkii.coursemanagementsystem.specification;

import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class GenericSpecificationsBuilder<T> {

    private final List<SearchCriteria> params = new ArrayList<>();

    public GenericSpecificationsBuilder<T> with(String key, String operation, Object value) {
        params.add(new SearchCriteria(key, operation, value));
        return this;
    }

    public GenericSpecificationsBuilder<T> with(SearchCriteria criteria) {
        params.add(criteria);
        return this;
    }

    public GenericSpecificationsBuilder<T> withSearchQuery(String search) {
        if (search == null || search.trim().isEmpty()) {
            return this;
        }
        // Match patterns: key>=val, key<=val, key!=val, key>val, key<val, key:val, key!val separated by comma
        Pattern pattern = Pattern.compile("([a-zA-Z0-9_.]+?)(>=|<=|!=|!|:|>|<)([a-zA-Z0-9_.@\\s\\p{L}-]+?)(?:,|$)");
        Matcher matcher = pattern.matcher(search);
        while (matcher.find()) {
            String key = matcher.group(1).trim();
            String op = matcher.group(2).trim();
            String value = matcher.group(3).trim();
            with(key, op, value);
        }
        return this;
    }

    public Specification<T> build() {
        if (params.isEmpty()) {
            return null;
        }

        Specification<T> result = new GenericSpecification<>(params.get(0));
        for (int i = 1; i < params.size(); i++) {
            result = Specification.where(result).and(new GenericSpecification<>(params.get(i)));
        }
        return result;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/SearchCriteria.java`

```java
package com.mkii.coursemanagementsystem.specification;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchCriteria {
    private String key;
    private String operation;
    private Object value;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/util/AESUtil.java`

```java
package com.mkii.coursemanagementsystem.util;

import javax.crypto.*;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Base64;

/**
 * Technical helper utility providing static methods for AES Encryption and Decryption,
 * key generation, password-based key derivation (PBKDF2), initialization vectors (IV),
 * String, File, and SealedObject operations.
 *
 * Implemented based on official Baeldung Java AES Encryption and Decryption standards.
 */
public final class AESUtil {

    public static final String DEFAULT_ALGORITHM = "AES/CBC/PKCS5Padding";
    public static final String GCM_ALGORITHM = "AES/GCM/NoPadding";
    public static final int GCM_TAG_LENGTH = 128;
    public static final int DEFAULT_IV_SIZE = 16;
    public static final int GCM_IV_SIZE = 12;
    public static final int PBKDF2_ITERATIONS = 65536;
    public static final int PBKDF2_KEY_LENGTH = 256;

    private AESUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Generates a random AES SecretKey with the specified bit size (128, 192, 256).
     */
    public static SecretKey generateKey(int n) throws NoSuchAlgorithmException {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(n);
        return keyGenerator.generateKey();
    }

    /**
     * Derives an AES SecretKey from a given password and salt using PBKDF2WithHmacSHA256.
     */
    public static SecretKey getKeyFromPassword(String password, String salt)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        if (password == null || salt == null) {
            throw new IllegalArgumentException("Password and salt cannot be null");
        }
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(StandardCharsets.UTF_8), PBKDF2_ITERATIONS, PBKDF2_KEY_LENGTH);
        return new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
    }

    /**
     * Generates a cryptographically random 16-byte Initialization Vector (IV) for CBC mode.
     */
    public static IvParameterSpec generateIv() {
        byte[] iv = new byte[DEFAULT_IV_SIZE];
        new SecureRandom().nextBytes(iv);
        return new IvParameterSpec(iv);
    }

    /**
     * Generates a cryptographically random 12-byte IV for GCM mode with 128-bit authentication tag.
     */
    public static GCMParameterSpec generateGcmIv() {
        byte[] iv = new byte[GCM_IV_SIZE];
        new SecureRandom().nextBytes(iv);
        return new GCMParameterSpec(GCM_TAG_LENGTH, iv);
    }

    /**
     * Encrypts a plaintext String using AES with IvParameterSpec (e.g. CBC mode) and returns Base64 ciphertext.
     */
    public static String encrypt(String algorithm, String input, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] cipherText = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(cipherText);
    }

    /**
     * Decrypts a Base64 ciphertext String using AES with IvParameterSpec (e.g. CBC mode).
     */
    public static String decrypt(String algorithm, String cipherText, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (cipherText == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText, StandardCharsets.UTF_8);
    }

    /**
     * Encrypts a plaintext String using AES with GCMParameterSpec (e.g. GCM mode) and returns Base64 ciphertext.
     */
    public static String encryptGcm(String input, SecretKey key, GCMParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(GCM_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] cipherText = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(cipherText);
    }

    /**
     * Decrypts a Base64 ciphertext String using AES with GCMParameterSpec (e.g. GCM mode).
     */
    public static String decryptGcm(String cipherText, SecretKey key, GCMParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (cipherText == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(GCM_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText, StandardCharsets.UTF_8);
    }

    /**
     * Encrypts a Serializable Java Object into a SealedObject using AES.
     */
    public static SealedObject encryptObject(String algorithm, Serializable object, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, IOException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        return new SealedObject(object, cipher);
    }

    /**
     * Decrypts a SealedObject back into its original Serializable Java Object.
     */
    public static Serializable decryptObject(String algorithm, SealedObject sealedObject, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, ClassNotFoundException, BadPaddingException, IllegalBlockSizeException, IOException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        return (Serializable) sealedObject.getObject(cipher);
    }

    /**
     * Encrypts an input File to an output File using AES and stream buffering.
     */
    public static void encryptFile(String algorithm, SecretKey key, IvParameterSpec iv, File inputFile, File outputFile)
            throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        processFile(cipher, inputFile, outputFile);
    }

    /**
     * Decrypts an encrypted File to an output File using AES and stream buffering.
     */
    public static void decryptFile(String algorithm, SecretKey key, IvParameterSpec iv, File inputFile, File outputFile)
            throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        processFile(cipher, inputFile, outputFile);
    }

    private static void processFile(Cipher cipher, File inputFile, File outputFile)
            throws IOException, BadPaddingException, IllegalBlockSizeException {
        try (FileInputStream inputStream = new FileInputStream(inputFile);
             FileOutputStream outputStream = new FileOutputStream(outputFile)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                byte[] output = cipher.update(buffer, 0, bytesRead);
                if (output != null) {
                    outputStream.write(output);
                }
            }
            byte[] outputBytes = cipher.doFinal();
            if (outputBytes != null) {
                outputStream.write(outputBytes);
            }
        }
    }

    /**
     * Encrypts a raw byte array by generating a random 16-byte IV, encrypting the bytes,
     * and prepending the IV to the ciphertext [IV (16 bytes) | Encrypted payload].
     */
    public static byte[] encryptBytesWithIv(byte[] input, SecretKey key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        IvParameterSpec iv = generateIv();
        Cipher cipher = Cipher.getInstance(DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] encrypted = cipher.doFinal(input);
        byte[] result = new byte[DEFAULT_IV_SIZE + encrypted.length];
        System.arraycopy(iv.getIV(), 0, result, 0, DEFAULT_IV_SIZE);
        System.arraycopy(encrypted, 0, result, DEFAULT_IV_SIZE, encrypted.length);
        return result;
    }

    /**
     * Decrypts a raw byte array formatted as [IV (16 bytes) | Encrypted payload].
     */
    public static byte[] decryptBytesWithIv(byte[] input, SecretKey key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null || input.length <= DEFAULT_IV_SIZE) {
            return input;
        }
        byte[] ivBytes = new byte[DEFAULT_IV_SIZE];
        System.arraycopy(input, 0, ivBytes, 0, DEFAULT_IV_SIZE);
        IvParameterSpec iv = new IvParameterSpec(ivBytes);

        Cipher cipher = Cipher.getInstance(DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        return cipher.doFinal(input, DEFAULT_IV_SIZE, input.length - DEFAULT_IV_SIZE);
    }

    /**
     * Encrypts plaintext string with prepended IV and returns a Base64 encoded string.
     */
    public static String encryptStringWithIv(String plainText, SecretKey key) throws Exception {
        if (plainText == null) {
            return null;
        }
        byte[] encrypted = encryptBytesWithIv(plainText.getBytes(StandardCharsets.UTF_8), key);
        return Base64.getEncoder().encodeToString(encrypted);
    }

    /**
     * Decrypts a Base64 string that has prepended IV.
     */
    public static String decryptStringWithIv(String cipherText, SecretKey key) throws Exception {
        if (cipherText == null) {
            return null;
        }
        byte[] decoded = Base64.getDecoder().decode(cipherText);
        byte[] decrypted = decryptBytesWithIv(decoded, key);
        return new String(decrypted, StandardCharsets.UTF_8);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/util/DateTimeUtil.java`

```java
package com.mkii.coursemanagementsystem.util;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

/**
 * Technical helper utility providing static methods for date/time formatting,
 * parsing, and epoch millisecond conversions.
 * Contains purely technical methods without any business logic.
 */
public final class DateTimeUtil {

    public static final String DEFAULT_DATETIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
    public static final String DEFAULT_DATE_PATTERN = "yyyy-MM-dd";
    public static final String ISO_DATETIME_PATTERN = "yyyy-MM-dd'T'HH:mm:ss";

    private DateTimeUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Formats a LocalDateTime into a string with the specified pattern.
     */
    public static String format(LocalDateTime dateTime, String pattern) {
        if (dateTime == null) {
            return "";
        }
        String p = (pattern != null && !pattern.isEmpty()) ? pattern : DEFAULT_DATETIME_PATTERN;
        return dateTime.format(DateTimeFormatter.ofPattern(p));
    }

    /**
     * Parses a string into a LocalDateTime with the specified pattern.
     */
    public static LocalDateTime parse(String text, String pattern) {
        if (text == null || text.trim().isEmpty()) {
            return null;
        }
        String p = (pattern != null && !pattern.isEmpty()) ? pattern : DEFAULT_DATETIME_PATTERN;
        return LocalDateTime.parse(text.trim(), DateTimeFormatter.ofPattern(p));
    }

    /**
     * Converts a LocalDateTime to epoch milliseconds in the system default timezone.
     */
    public static long toEpochMillis(LocalDateTime dateTime) {
        if (dateTime == null) {
            return 0L;
        }
        return dateTime.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli();
    }

    /**
     * Converts epoch milliseconds to LocalDateTime in the system default timezone.
     */
    public static LocalDateTime fromEpochMillis(long epochMillis) {
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(epochMillis), ZoneId.systemDefault());
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/util/FileUtil.java`

```java
package com.mkii.coursemanagementsystem.util;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;
import java.util.regex.Pattern;

/**
 * Technical helper utility providing static methods for file name validation,
 * extension extraction, sanitization against path traversal, and byte size formatting.
 * Contains purely technical methods without any business logic.
 */
public final class FileUtil {

    private static final Pattern SAFE_FILENAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_.-]+$");
    private static final String[] SIZE_UNITS = new String[]{"B", "KB", "MB", "GB", "TB"};

    private FileUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Checks if a file name contains only safe characters (alphanumeric, dot, underscore, dash).
     * Returns true if safe, false if contains invalid/special characters.
     */
    public static boolean checkFileNameSpecialChar(String fileName) {
        if (fileName == null || fileName.trim().isEmpty()) {
            return false;
        }
        return SAFE_FILENAME_PATTERN.matcher(fileName.trim()).matches();
    }

    /**
     * Extracts the extension of a file name in lowercase (e.g. "document.PDF" -> "pdf").
     * Returns empty string if no extension is present.
     */
    public static String getFileExtension(String fileName) {
        if (fileName == null || fileName.lastIndexOf('.') == -1) {
            return "";
        }
        return fileName.substring(fileName.lastIndexOf('.') + 1).trim().toLowerCase();
    }

    /**
     * Sanitizes a file name by removing path traversal characters and illegal path separators.
     */
    public static String sanitizeFileName(String fileName) {
        if (fileName == null) {
            return "";
        }
        // Remove path traversal sequences and separators
        String clean = fileName.replaceAll("[\\\\/]+", "_")
                .replaceAll("\\.\\.+", ".")
                .trim();
        return clean.replaceAll("[^a-zA-Z0-9_.-]", "_");
    }

    /**
     * Formats raw bytes into human-readable representation (e.g. 1024 -> "1 KB", 1048576 -> "1 MB").
     */
    public static String formatFileSize(long bytes) {
        if (bytes <= 0) {
            return "0 B";
        }
        int digitGroups = (int) (Math.log10(bytes) / Math.log10(1024));
        if (digitGroups >= SIZE_UNITS.length) {
            digitGroups = SIZE_UNITS.length - 1;
        }
        return new DecimalFormat("#,##0.#", DecimalFormatSymbols.getInstance(Locale.ENGLISH))
                .format(bytes / Math.pow(1024, digitGroups)) + " " + SIZE_UNITS[digitGroups];
    }

    /**
     * Checks whether the file size is within acceptable threshold.
     */
    public static boolean isValidFileSize(long bytes, long maxBytes) {
        return bytes > 0 && bytes <= maxBytes;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/util/StringUtil.java`

```java
package com.mkii.coursemanagementsystem.util;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

/**
 * Technical helper utility providing static methods for string manipulation,
 * sensitive data masking, slug generation, and validation checks.
 * Contains purely technical methods without any business logic.
 */
public final class StringUtil {

    private static final Pattern NON_LATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");

    private StringUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    public static boolean isEmpty(CharSequence cs) {
        return cs == null || cs.length() == 0;
    }

    public static boolean isNotEmpty(CharSequence cs) {
        return !isEmpty(cs);
    }

    public static boolean isBlank(CharSequence cs) {
        if (cs == null) {
            return true;
        }
        for (int i = 0; i < cs.length(); i++) {
            if (!Character.isWhitespace(cs.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public static boolean isNotBlank(CharSequence cs) {
        return !isBlank(cs);
    }

    /**
     * Masks sensitive string content, keeping a prefix and suffix visible.
     * Example: maskSensitive("mysecrettoken123", 3, 3) -> "mys**********123"
     */
    public static String maskSensitive(String input, int startVisible, int endVisible) {
        if (input == null) {
            return null;
        }
        int len = input.length();
        if (len <= (startVisible + endVisible)) {
            return "*".repeat(len);
        }
        String prefix = input.substring(0, startVisible);
        String suffix = input.substring(len - endVisible);
        String masked = "*".repeat(len - startVisible - endVisible);
        return prefix + masked + suffix;
    }

    /**
     * Masks an email address for privacy.
     * Example: "student@example.com" -> "s***t@example.com"
     */
    public static String maskEmail(String email) {
        if (email == null || !email.contains("@")) {
            return maskSensitive(email, 1, 1);
        }
        String[] parts = email.split("@", 2);
        String name = parts[0];
        String domain = parts[1];
        if (name.length() <= 2) {
            return "*".repeat(name.length()) + "@" + domain;
        }
        return name.charAt(0) + "*".repeat(name.length() - 2) + name.charAt(name.length() - 1) + "@" + domain;
    }

    /**
     * Generates a clean URL slug from text (supporting Vietnamese diacritics).
     * Example: "Khóa học Lập trình Java 2026!" -> "khoa-hoc-lap-trinh-java-2026"
     */
    public static String toSlug(String input) {
        if (input == null || input.trim().isEmpty()) {
            return "";
        }
        String normalized = Normalizer.normalize(input, Normalizer.Form.NFD);
        String noDiacritics = Pattern.compile("\\p{InCombiningDiacriticalMarks}+").matcher(normalized).replaceAll("");
        noDiacritics = noDiacritics.replace("đ", "d").replace("Đ", "D");
        String noWhitespace = WHITESPACE.matcher(noDiacritics).replaceAll("-");
        String slug = NON_LATIN.matcher(noWhitespace).replaceAll("");
        return slug.toLowerCase(Locale.ENGLISH).replaceAll("-+", "-").replaceAll("^-|-$", "");
    }
}
```

---

## File: `src/main/resources/application.properties`

```properties
spring.application.name=course-management-system

# Datasource Configuration (Hỗ trợ cả Localhost và Docker Container)
spring.datasource.url=${SPRING_DATASOURCE_URL:jdbc:mysql://localhost:3306/course_db?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC}
spring.datasource.username=${SPRING_DATASOURCE_USERNAME:root}
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD:123456}
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# HikariCP Connection Pool Optimization
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=30000
spring.datasource.hikari.connection-timeout=20000
spring.datasource.hikari.max-lifetime=1800000

# JPA & Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false

# Encoding Configuration
server.servlet.encoding.charset=UTF-8
server.servlet.encoding.enabled=true
server.servlet.encoding.force=true

# MinIO Object Storage Configuration (Hỗ trợ cả Localhost và Docker Container)
minio.endpoint=${MINIO_ENDPOINT:http://localhost:9000}
minio.access-key=${MINIO_ACCESS_KEY:minioadmin}
minio.secret-key=${MINIO_SECRET_KEY:minioadmin}
minio.bucket-name=${MINIO_BUCKET_NAME:documents}

# Multipart File Upload Limits
spring.servlet.multipart.max-file-size=50MB
spring.servlet.multipart.max-request-size=100MB

# JWT & AES Security Configuration
jwt.secret=${JWT_SECRET:9a4f2c8d3b7a1e6f4c8b2d0e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a}
jwt.expiration=${JWT_EXPIRATION:86400000}
cms.security.aes-key=${CMS_AES_KEY:CourseManagementSystemSecretKey2026}
cms.security.aes-salt=${CMS_AES_SALT:cms-salt-2026-v1}
```

---

