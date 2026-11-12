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

    // Enrollment Validation Messages
    public static final String ENROLLMENT_NOT_FOUND = "Không tìm thấy lượt ghi danh với ID: %d";
    public static final String ENROLLMENT_ALREADY_EXISTS = "Sinh viên (ID: %d) đã ghi danh khóa học (ID: %d) trước đó.";
    public static final String ENROLLMENT_DELETED_SUCCESS = "Xóa lượt ghi danh thành công";

    // Storage (MinIO) Messages
    public static final String MINIO_CONNECT_FAILED = "Could not connect to MinIO storage: %s";
    public static final String MINIO_UPLOAD_FAILED = "Failed to upload file to MinIO: %s";
    public static final String MINIO_DOWNLOAD_FAILED = "Failed to download file from MinIO: %s";
    public static final String MINIO_DELETE_FAILED = "Failed to delete file from MinIO: %s";
}