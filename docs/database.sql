-- ======================================================================
-- SCRIPT CSDL MYSQL CHO HỆ THỐNG COURSE MANAGEMENT SYSTEM & EDU PORTAL
-- Tác giả: Nguyễn Duy Trường
-- ======================================================================

CREATE DATABASE IF NOT EXISTS course_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE course_db;

-- 1. BẢNG KHOA / NGÀNH (departments)
CREATE TABLE IF NOT EXISTS departments (
    department_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    department_code VARCHAR(20) NOT NULL UNIQUE,
    department_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    created_at DATETIME(6),
    updated_at DATETIME(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. BẢNG NGƯỜI DÙNG / TÀI KHOẢN (users)
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'USER',
    created_at DATETIME(6),
    updated_at DATETIME(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. BẢNG KHÓA HỌC (courses)
CREATE TABLE IF NOT EXISTS courses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL UNIQUE,
    description VARCHAR(255),
    duration INT NOT NULL,
    price DOUBLE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. BẢNG SINH VIÊN (students)
CREATE TABLE IF NOT EXISTS students (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    dob DATE,
    department_id BIGINT,
    CONSTRAINT fk_students_department FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. BẢNG TÀI LIỆU MINIO (tbl_document)
CREATE TABLE IF NOT EXISTS tbl_document (
    id VARCHAR(36) PRIMARY KEY,
    APP_DETAIL_FK VARCHAR(50) NOT NULL COMMENT 'Mã nghiệp vụ liên kết (Student ID, Course ID)',
    NAME VARCHAR(255) NOT NULL,
    PATH VARCHAR(500) NOT NULL,
    OWNER VARCHAR(100),
    VERSION DOUBLE DEFAULT 1.0,
    DELETED BOOLEAN DEFAULT FALSE,
    CREATED_TIME DATETIME(6),
    MODIFIED_TIME DATETIME(6),
    ACTIVE BOOLEAN DEFAULT TRUE,
    INDEX idx_doc_app (APP_DETAIL_FK),
    INDEX idx_doc_deleted (DELETED)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ======================================================================
-- DỮ LIỆU MẪU BAN ĐẦU (SEED DATA)
-- ======================================================================

-- Khoa / Ngành mẫu
INSERT INTO departments (department_code, department_name, description, created_at, updated_at) VALUES
('CNTT', 'Công nghệ thông tin', 'Khoa Công nghệ thông tin & Truyền thông', NOW(), NOW()),
('KHMT', 'Khoa học máy tính', 'Khoa Khoa học máy tính & Trí tuệ nhân tạo', NOW(), NOW()),
('QTKD', 'Quản trị kinh doanh', 'Khoa Quản trị kinh doanh & Kinh tế số', NOW(), NOW())
ON DUPLICATE KEY UPDATE department_name=VALUES(department_name);

-- Tài khoản mẫu (Mật khẩu đã mã hóa BCrypt cho: 123456)
INSERT INTO users (username, password, email, full_name, role, created_at, updated_at) VALUES
('admin', '$2a$10$7R0Zqg7y0sYF6wM51K3/Ue3oZg6e1x8Z5m3y2K1j0a9b8c7d6e5f.', 'admin@school.edu.vn', 'Quản Trị Viên Hệ Thống', 'ADMIN', NOW(), NOW()),
('gv_nam', '$2a$10$7R0Zqg7y0sYF6wM51K3/Ue3oZg6e1x8Z5m3y2K1j0a9b8c7d6e5f.', 'nam@school.edu.vn', 'ThS. Nguyễn Văn Nam', 'TEACHER', NOW(), NOW()),
('student_a', '$2a$10$7R0Zqg7y0sYF6wM51K3/Ue3oZg6e1x8Z5m3y2K1j0a9b8c7d6e5f.', 'student_a@school.edu.vn', 'Nguyễn Văn A', 'USER', NOW(), NOW())
ON DUPLICATE KEY UPDATE email=VALUES(email);

-- Khóa học mẫu
INSERT INTO courses (title, description, duration, price) VALUES
('Lập trình Spring Boot 3 & Hibernate DAO Chuyên Sâu', 'Khóa học thực chiến từ kiến trúc Generic DAO đến REST API và MinIO', 60, 499.0),
('Xây dựng Trợ lý AI Chuyên Biệt với PyTorch & QLoRA', 'Tự động tinh chỉnh mô hình mã nguồn mở Qwen trên GPU cục bộ', 45, 699.0),
('Kiến trúc Hệ thống Phân tán & Lưu trữ Đám mây MinIO', 'Lưu trữ phi cấu trúc, xử lý tệp đa luồng và bảo mật dữ liệu', 30, 350.0)
ON DUPLICATE KEY UPDATE description=VALUES(description);

-- Sinh viên mẫu
INSERT INTO students (full_name, email, phone, address, dob, department_id) VALUES
('Nguyễn Văn A', 'vana@gmail.com', '0912345678', 'Hà Nội', '2003-05-15', 1),
('Trần Thị B', 'thib@gmail.com', '0987654321', 'Đà Nẵng', '2004-08-20', 2),
('Lê Văn C', 'vanc@gmail.com', '0905123456', 'TP. Hồ Chí Minh', '2002-11-10', 3)
ON DUPLICATE KEY UPDATE phone=VALUES(phone);
