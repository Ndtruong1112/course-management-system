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
