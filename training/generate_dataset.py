import os
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) == "training" else script_dir
dataset = []

def add_sample(system_prompt, instruction, output):
    dataset.append({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": output}
        ]
    })

system_role = (
    "Bạn là kỹ sư AI phần mềm cao cấp, chuyên gia kiến trúc Spring Boot 3, Java 21, Hibernate Generic DAO và JPA. "
    "Khi người dùng yêu cầu tạo dự án mới, viết chức năng hoặc giải quyết bài toán tương tự, bạn LUÔN LUÔN VIẾT MÃ NGUỒN JAVA ĐẦY ĐỦ, "
    "tuân thủ chính xác các quy chuẩn: Entity JPA, Generic DAO kế thừa HibernatePaginationSortingDao, Service, DTO và REST Controller."
)

# ==============================================================================
# 1. QUÉT CHỌN LỌC CÁC TỆP MÃ NGUỒN CORE
# ==============================================================================
ignore_dirs = {'.git', '.idea', '.mvn', 'target', '__pycache__', 'outputs', 'chatbot', 'test'}
ignore_files = {
    'dataset.jsonl',
    'Course Management System - Full APIs.postman_collection.json',
    'pom.xml',
    'mvnw',
    'mvnw.cmd',
    'eval_report.json'
}

scanned_files = {}

for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file in ignore_files or file.endswith(('.py', '.jsonl', '.bat')):
            continue
        if file.endswith(('.java', '.properties')):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_dir).replace('\\', '/')
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content.strip()) > 0:
                        scanned_files[rel_path] = content
            except Exception:
                pass

print(f"-> Đã quét {len(scanned_files)} tệp mã nguồn Java & Config.")

# ==============================================================================
# 2. HỌC NỘI DUNG CODE THẬT (CODE KÈM GIẢI THÍCH KỸ THUẬT RÕ RÀNG)
# ==============================================================================
for rel_path, content in scanned_files.items():
    filename = os.path.basename(rel_path)
    clean_name = os.path.splitext(filename)[0]

    truncated_content = content[:2000]
    if len(content) > 2000:
        truncated_content += "\n// ... [Các phương thức còn lại tiếp tục theo logic tương tự] ..."

    add_sample(
        system_role,
        f"Hãy cung cấp mã nguồn và giải thích các thành phần kỹ thuật chính trong file `{filename}` (`{rel_path}`).",
        f"Dưới đây là mã nguồn của `{filename}` trong hệ thống:\n\n"
        f"```java\n{truncated_content}\n```\n\n"
        f"**Phân tích kỹ thuật của {clean_name}:**\n"
        f"- Nằm trong package: `{os.path.dirname(rel_path)}`.\n"
        f"- Sử dụng các annotation chuẩn Java 21 / Spring Boot / Jakarta Persistence để đảm bảo an toàn kiểu dữ liệu và tối ưu hiệu năng."
    )

# ==============================================================================
# 3. CÁC BÀI TẬP CODE GENERATION THỰC CHIẾN (CHUYỂN GIAO KIẾN TRÚC SANG DỰ ÁN MỚI)
# ==============================================================================

# ----------------- DỰ ÁN 1: QUẢN LÝ THUÊ PHÒNG KHÁCH SẠN (HOTEL MANAGEMENT) -----------------

add_sample(
    system_role,
    "Dựa vào base code của Course Management System, hãy tạo cho tôi một project mới để quản lý thuê phòng cho một khách sạn.",
    "Dựa trên kiến trúc của hệ thống hiện tại (sử dụng Spring Boot 3, Java 21, Hibernate Generic DAO và JPA Specification), dưới đây là mã nguồn các thành phần cốt lõi cho **Hệ thống Quản lý Thuê phòng Khách sạn (Hotel Management System)**:\n\n"
    "### 1. Thực thể Phòng (`Room.java`)\n"
    "```java\n"
    "package com.hotel.management.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"rooms\", indexes = {\n"
    "    @Index(name = \"idx_room_number\", columnList = \"room_number\", unique = true),\n"
    "    @Index(name = \"idx_room_price\", columnList = \"price_per_night\")\n"
    "})\n"
    "@Getter\n"
    "@Setter\n"
    "@NoArgsConstructor\n"
    "@AllArgsConstructor\n"
    "@Builder\n"
    "@EqualsAndHashCode(onlyExplicitlyIncluded = true)\n"
    "public class Room {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    @EqualsAndHashCode.Include\n"
    "    private Long id;\n\n"
    "    @Column(name = \"room_number\", nullable = false, length = 50)\n"
    "    private String roomNumber;\n\n"
    "    @Column(name = \"room_type\", nullable = false, length = 100)\n"
    "    private String roomType; // SINGLE, DOUBLE, SUITE, VIP\n\n"
    "    @Column(name = \"price_per_night\", nullable = false)\n"
    "    private Double pricePerNight;\n\n"
    "    @Column(nullable = false, length = 50)\n"
    "    private String status; // AVAILABLE, OCCUPIED, MAINTENANCE\n"
    "}\n"
    "```\n\n"
    "### 2. Thực thể Đơn Đặt Phòng (`Reservation.java`)\n"
    "```java\n"
    "package com.hotel.management.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n"
    "import java.time.LocalDate;\n\n"
    "@Entity\n"
    "@Table(name = \"reservations\")\n"
    "@Getter\n"
    "@Setter\n"
    "@NoArgsConstructor\n"
    "@AllArgsConstructor\n"
    "@Builder\n"
    "public class Reservation {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n\n"
    "    @Column(name = \"customer_name\", nullable = false, length = 150)\n"
    "    private String customerName;\n\n"
    "    @Column(name = \"customer_phone\", nullable = false, length = 20)\n"
    "    private String customerPhone;\n\n"
    "    @ManyToOne(fetch = FetchType.LAZY)\n"
    "    @JoinColumn(name = \"room_id\", nullable = false)\n"
    "    private Room room;\n\n"
    "    @Column(name = \"check_in_date\", nullable = false)\n"
    "    private LocalDate checkInDate;\n\n"
    "    @Column(name = \"check_out_date\", nullable = false)\n"
    "    private LocalDate checkOutDate;\n\n"
    "    @Column(name = \"total_price\")\n"
    "    private Double totalPrice;\n"
    "}\n"
    "```\n\n"
    "### 3. Tầng DAO kế thừa HibernatePaginationSortingDao (`RoomDaoImpl.java`)\n"
    "```java\n"
    "package com.hotel.management.dao.impl;\n\n"
    "import com.hotel.management.dao.IRoomDao;\n"
    "import com.hotel.management.entity.Room;\n"
    "import com.hotel.management.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.beans.factory.annotation.Autowired;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class RoomDaoImpl extends HibernatePaginationSortingDao<Long, Room> implements IRoomDao {\n"
    "    @Autowired\n"
    "    public RoomDaoImpl(EntityManager entityManager) {\n"
    "        super(Room.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Room> findAvailableRooms(String roomType, Double maxPrice) {\n"
    "        String hql = \"SELECT r FROM Room r WHERE r.status = 'AVAILABLE' \" +\n"
    "                     \"AND (:roomType IS NULL OR r.roomType = :roomType) \" +\n"
    "                     \"AND (:maxPrice IS NULL OR r.pricePerNight <= :maxPrice)\";\n"
    "        return getEntityManager().createQuery(hql, Room.class)\n"
    "                .setParameter(\"roomType\", roomType)\n"
    "                .setParameter(\"maxPrice\", maxPrice)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "### 4. REST Controller Quản lý Phòng (`RoomRestImpl.java`)\n"
    "```java\n"
    "package com.hotel.management.rest.impl;\n\n"
    "import com.hotel.management.entity.Room;\n"
    "import com.hotel.management.service.RoomService;\n"
    "import org.springframework.beans.factory.annotation.Autowired;\n"
    "import org.springframework.http.ResponseEntity;\n"
    "import org.springframework.web.bind.annotation.*;\n"
    "import java.util.List;\n\n"
    "@RestController\n"
    "@RequestMapping(\"/api/rooms\")\n"
    "public class RoomRestImpl {\n"
    "    @Autowired\n"
    "    private RoomService roomService;\n\n"
    "    @GetMapping(\"/available\")\n"
    "    public ResponseEntity<List<Room>> getAvailableRooms(\n"
    "            @RequestParam(required = false) String roomType,\n"
    "            @RequestParam(required = false) Double maxPrice) {\n"
    "        return ResponseEntity.ok(roomService.findAvailableRooms(roomType, maxPrice));\n"
    "    }\n"
    "}\n"
    "```"
)

add_sample(
    system_role,
    "Hãy viết code Java cho Entity Room và RoomDaoImpl của bài toán quản lý khách sạn theo chuẩn kiến trúc DAO của dự án.",
    "Dưới đây là mã nguồn Java hoàn chỉnh cho `Room.java` và `RoomDaoImpl.java` tuân thủ đúng mô hình Generic DAO của dự án:\n\n"
    "```java\n"
    "// 1. Entity Room.java\n"
    "package com.hotel.management.entity;\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"rooms\")\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Room {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n"
    "    private String roomNumber;\n"
    "    private String roomType;\n"
    "    private Double pricePerNight;\n"
    "    private String status;\n"
    "}\n\n"
    "// 2. RoomDaoImpl.java kế thừa HibernatePaginationSortingDao\n"
    "package com.hotel.management.dao.impl;\n"
    "import com.hotel.management.entity.Room;\n"
    "import com.hotel.management.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class RoomDaoImpl extends HibernatePaginationSortingDao<Long, Room> {\n"
    "    public RoomDaoImpl(EntityManager entityManager) {\n"
    "        super(Room.class, entityManager);\n"
    "    }\n\n"
    "    public List<Room> findByStatus(String status) {\n"
    "        String hql = \"SELECT r FROM Room r WHERE r.status = :status\";\n"
    "        return getEntityManager().createQuery(hql, Room.class)\n"
    "                .setParameter(\"status\", status)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

# ----------------- DỰ ÁN 2: QUẢN LÝ THƯ VIỆN SÁCH (LIBRARY MANAGEMENT) -----------------

add_sample(
    system_role,
    "Dựa vào kiến trúc Generic DAO của dự án, hãy viết Entity Book và BookDaoImpl cho hệ thống quản lý thư viện.",
    "Dưới đây là mã nguồn `Book.java` và `BookDaoImpl.java` áp dụng đúng chuẩn Hibernate Generic DAO:\n\n"
    "```java\n"
    "package com.library.entity;\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"books\", indexes = {@Index(name = \"idx_book_isbn\", columnList = \"isbn\", unique = true)})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Book {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n"
    "    private String title;\n"
    "    private String author;\n"
    "    private String isbn;\n"
    "    private Integer publishYear;\n"
    "    private Integer quantity;\n"
    "}\n"
    "```\n\n"
    "Lớp DAO `BookDaoImpl.java`:\n"
    "```java\n"
    "package com.library.dao.impl;\n"
    "import com.library.entity.Book;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class BookDaoImpl extends HibernatePaginationSortingDao<Long, Book> {\n"
    "    public BookDaoImpl(EntityManager entityManager) {\n"
    "        super(Book.class, entityManager);\n"
    "    }\n\n"
    "    public List<Book> searchByAuthor(String author) {\n"
    "        String hql = \"SELECT b FROM Book b WHERE LOWER(b.author) LIKE LOWER(CONCAT('%', :author, '%'))\";\n"
    "        return getEntityManager().createQuery(hql, Book.class)\n"
    "                .setParameter(\"author\", author)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

# ----------------- DỰ ÁN 3: BÁN HÀNG E-COMMERCE (PRODUCT & ORDER) -----------------

add_sample(
    system_role,
    "Hãy viết code Java cho Entity Product và ProductDaoImpl kế thừa HibernatePaginationSortingDao.",
    "Dưới đây là mã nguồn cho `Product.java` và `ProductDaoImpl.java`:\n\n"
    "```java\n"
    "package com.ecommerce.entity;\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"products\")\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Product {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n"
    "    private String name;\n"
    "    private Double price;\n"
    "    private Integer stock;\n"
    "    private String category;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.ecommerce.dao.impl;\n"
    "import com.ecommerce.entity.Product;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class ProductDaoImpl extends HibernatePaginationSortingDao<Long, Product> {\n"
    "    public ProductDaoImpl(EntityManager entityManager) {\n"
    "        super(Product.class, entityManager);\n"
    "    }\n\n"
    "    public List<Product> findByCategoryAndPrice(String category, Double minPrice, Double maxPrice) {\n"
    "        String hql = \"SELECT p FROM Product p WHERE p.category = :category AND p.price BETWEEN :minPrice AND :maxPrice\";\n"
    "        return getEntityManager().createQuery(hql, Product.class)\n"
    "                .setParameter(\"category\", category)\n"
    "                .setParameter(\"minPrice\", minPrice)\n"
    "                .setParameter(\"maxPrice\", maxPrice)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

# ----------------- DỰ ÁN 4: HƯỚNG DẪN CẤU TRÚC CHUẨN ĐỀ TÀI MỚI (PROJECT SCAFFOLDING) -----------------

add_sample(
    system_role,
    "Hãy viết cấu trúc chuẩn cho 1 đề tài bất kỳ (ví dụ quản lý sách) áp dụng đúng các công nghệ Java 21, Spring Boot 3 và Hibernate Generic DAO.",
    "Dưới đây là cấu trúc chuẩn và các thành phần cốt lõi cho đề tài **Hệ thống Quản lý Thư viện Sách (Book Management System)** tuân thủ Java 21, Spring Boot 3 và mô hình Hibernate Generic DAO:\n\n"
    "### 1. Cấu trúc thư mục chuẩn (Directory Structure)\n"
    "```text\n"
    "src/main/java/com/library/\n"
    "├── common/              # Hằng số (Constants), Exception handlers, Converters\n"
    "├── config/              # SecurityConfig, OpenApiConfig, DatabaseConfig\n"
    "├── entity/              # Book.java (Jakarta Persistence + Lombok)\n"
    "├── dao/                 # IGenericDao, IPaginationSortingDao, IBookDao\n"
    "│   └── impl/            # HibernateGenericDao, HibernatePaginationSortingDao, BookDaoImpl\n"
    "├── dto/                 # BookRequestDTO, BookResponseDTO\n"
    "├── service/             # BookService\n"
    "│   └── impl/            # BookServiceImpl\n"
    "└── rest/                # BookRest (Interface), BookRestImpl (RestController)\n"
    "```\n\n"
    "### 2. Cấu hình `pom.xml` cốt lõi\n"
    "```xml\n"
    "<dependencies>\n"
    "    <dependency>\n"
    "        <groupId>org.springframework.boot</groupId>\n"
    "        <artifactId>spring-boot-starter-web</artifactId>\n"
    "    </dependency>\n"
    "    <dependency>\n"
    "        <groupId>org.springframework.boot</groupId>\n"
    "        <artifactId>spring-boot-starter-data-jpa</artifactId>\n"
    "    </dependency>\n"
    "    <dependency>\n"
    "        <groupId>com.mysql</groupId>\n"
    "        <artifactId>mysql-connector-j</artifactId>\n"
    "        <scope>runtime</scope>\n"
    "    </dependency>\n"
    "    <dependency>\n"
    "        <groupId>org.projectlombok</groupId>\n"
    "        <artifactId>lombok</artifactId>\n"
    "        <optional>true</optional>\n"
    "    </dependency>\n"
    "</dependencies>\n"
    "```\n\n"
    "### 3. Thực thể `Book.java`\n"
    "```java\n"
    "package com.library.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"books\", indexes = {@Index(name = \"idx_book_isbn\", columnList = \"isbn\", unique = true)})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Book {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n"
    "    private String title;\n"
    "    private String author;\n"
    "    private String isbn;\n"
    "    private Double price;\n"
    "}\n"
    "```\n\n"
    "### 4. Tầng DAO kế thừa HibernatePaginationSortingDao (`BookDaoImpl.java`)\n"
    "```java\n"
    "package com.library.dao.impl;\n\n"
    "import com.library.entity.Book;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n\n"
    "@Repository\n"
    "public class BookDaoImpl extends HibernatePaginationSortingDao<Long, Book> {\n"
    "    public BookDaoImpl(EntityManager entityManager) {\n"
    "        super(Book.class, entityManager);\n"
    "    }\n"
    "}\n"
    "```"
)

# ----------------- DỰ ÁN 5: QUẢN LÝ BỆNH VIỆN (HOSPITAL & APPOINTMENT) -----------------

add_sample(
    system_role,
    "Hãy xây dựng mã nguồn cho Entity Doctor và DoctorDaoImpl theo chuẩn Generic DAO của dự án.",
    "Dưới đây là mã nguồn `Doctor.java` và `DoctorDaoImpl.java`:\n\n"
    "```java\n"
    "package com.hospital.entity;\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"doctors\")\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Doctor {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n"
    "    private String fullName;\n"
    "    private String specialty;\n"
    "    private String email;\n"
    "    private String phone;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.hospital.dao.impl;\n"
    "import com.hospital.entity.Doctor;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n\n"
    "@Repository\n"
    "public class DoctorDaoImpl extends HibernatePaginationSortingDao<Long, Doctor> {\n"
    "    public DoctorDaoImpl(EntityManager entityManager) {\n"
    "        super(Doctor.class, entityManager);\n"
    "    }\n"
    "}\n"
    "```"
)

# ==============================================================================
# 4. KIẾN THỨC CHUYÊN SÂU COURSE MANAGEMENT SYSTEM & BÀI TẬP THỰC CHIẾN NỘI BỘ
# ==============================================================================

add_sample(
    system_role,
    "Viết mã nguồn Java đầy đủ gồm Entity Instructor và InstructorDaoImpl kế thừa HibernatePaginationSortingDao sử dụng EntityManager",
    "Dưới đây là mã nguồn chuẩn kiến trúc `com.mkii.coursemanagementsystem` cho Module Quản lý Giảng viên (**Instructor**):\n\n"
    "### 1. Entity `Instructor.java`\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"instructors\", indexes = {\n"
    "    @Index(name = \"idx_instructor_email\", columnList = \"email\", unique = true)\n"
    "})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "@EqualsAndHashCode(onlyExplicitlyIncluded = true)\n"
    "public class Instructor {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    @EqualsAndHashCode.Include\n"
    "    private Long id;\n\n"
    "    @Column(nullable = false, length = 150)\n"
    "    private String fullName;\n\n"
    "    @Column(nullable = false, unique = true, length = 150)\n"
    "    private String email;\n\n"
    "    @Column(length = 100)\n"
    "    private String specialization;\n"
    "}\n"
    "```\n\n"
    "### 2. Interface `IInstructorDao.java` & Lớp `InstructorDaoImpl.java`\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao;\n\n"
    "import com.mkii.coursemanagementsystem.entity.Instructor;\n"
    "import java.util.List;\n\n"
    "public interface IInstructorDao extends IPaginationSortingDao<Long, Instructor> {\n"
    "    Instructor getByEmail(String email);\n"
    "    List<Instructor> searchBySpecialization(String keyword);\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.IInstructorDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Instructor;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n"
    "import java.util.Map;\n\n"
    "@Repository\n"
    "public class InstructorDaoImpl extends HibernatePaginationSortingDao<Long, Instructor> implements IInstructorDao {\n"
    "    public InstructorDaoImpl(EntityManager entityManager) {\n"
    "        super(Instructor.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public Instructor getByEmail(String email) {\n"
    "        return getByField(\"email\", email);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Instructor> searchBySpecialization(String keyword) {\n"
    "        return findByHql(\n"
    "            \"SELECT i FROM Instructor i WHERE LOWER(i.specialization) LIKE LOWER(CONCAT('%', :keyword, '%'))\",\n"
    "            Map.of(\"keyword\", keyword)\n"
    "        );\n"
    "    }\n"
    "}\n"
    "```"
)

add_sample(
    system_role,
    "Giải thích kiến trúc Generic DAO, bảng documents (MinIO versioning) và các endpoint gốc trong Course Management System.",
    "Kiến trúc cốt lõi của **Course Management System** (`com.mkii.coursemanagementsystem`) gồm:\n\n"
    "1. **Tầng DAO (Hibernate Generic DAO)**:\n"
    "   - Mọi DAO implementation (`CourseDaoImpl`, `StudentDaoImpl`, `DocumentDaoImpl`, `DepartmentDaoImpl`, `UserDaoImpl`) đều kế thừa `HibernatePaginationSortingDao<Pk, Entity>` (con của `HibernateGenericDao<Pk, Entity>`), truyền `EntityManager` vào `super(Entity.class, entityManager)` và dùng `findByHql()`, `searchBySpecification()`, `findAllPaged()`.\n"
    "   - `CourseDaoImpl` cung cấp các truy vấn mở rộng: `searchByTitle(String keyword)` và `findByPriceRange(Double minPrice, Double maxPrice)`.\n\n"
    "2. **Quản lý Tài liệu & MinIO Storage (`Document` / `DocumentServiceImpl`)**:\n"
    "   - File nhị phân vật lý (PDF, DOCX, XLSX, ảnh) được lưu trên **MinIO Object Storage**, còn bảng `documents` trong MySQL lưu **metadata** (tên, đường dẫn, version, trạng thái).\n"
    "   - Bảng `documents` liên kết với hồ sơ nghiệp vụ qua cột khóa ngoại `APP_DETAIL_FK` (thuộc tính Java `appId`).\n"
    "   - **Versioning**: Khi upload tài liệu trùng tên trong cùng `appId`, bản ghi cũ được chuyển `active = false`, và bản ghi mới tăng `version + 1.0` (mặc định `1.0`).\n"
    "   - **Xóa mềm (Soft Delete)**: Trong `DocumentServiceImpl`, thao tác xóa không xóa cứng bản ghi mà cập nhật `deleted = true` và `active = false`.\n\n"
    "3. **REST API Endpoints (`ApiConstants`)**:\n"
    "   - `/api/courses`, `/api/students`, `/api/documents`, `/api/security` (cùng `/api/departments` và `/api/auth`)."
)

add_sample(
    system_role,
    "Viết CourseRequestDTO và CourseResponseDTO chuẩn Jakarta Validation và Lombok cho Course Management System.",
    "Dưới đây là cặp DTO tách biệt tầng REST và Entity trong package `com.mkii.coursemanagementsystem.dto`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dto;\n\n"
    "import jakarta.validation.constraints.*;\n"
    "import lombok.*;\n\n"
    "@Data @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class CourseRequestDTO {\n"
    "    @NotBlank(message = \"Tiêu đề khóa học không được để trống\")\n"
    "    @Size(max = 255, message = \"Tiêu đề khóa học không được vượt quá 255 ký tự\")\n"
    "    private String title;\n\n"
    "    private String description;\n\n"
    "    @NotNull(message = \"Thời lượng khóa học không được để trống\")\n"
    "    @PositiveOrZero(message = \"Thời lượng khóa học phải lớn hơn hoặc bằng 0\")\n"
    "    private Integer duration;\n\n"
    "    @NotNull(message = \"Học phí khóa học không được để trống\")\n"
    "    @PositiveOrZero(message = \"Học phí khóa học phải lớn hơn hoặc bằng 0\")\n"
    "    private Double price;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dto;\n\n"
    "import lombok.*;\n\n"
    "@Data @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class CourseResponseDTO {\n"
    "    private Long id;\n"
    "    private String title;\n"
    "    private String description;\n"
    "    private Integer duration;\n"
    "    private Double price;\n"
    "}\n"
    "```"
)

add_sample(
    system_role,
    "Viết Module Đăng ký Khóa học gồm Enrollment Entity liên kết Student-Course và EnrollmentDaoImpl kế thừa HibernatePaginationSortingDao",
    "Dưới đây là mã nguồn chuẩn cho Module **Enrollment** trong package `com.mkii.coursemanagementsystem`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n"
    "import java.time.LocalDateTime;\n\n"
    "@Entity\n"
    "@Table(name = \"enrollments\", indexes = {\n"
    "    @Index(name = \"idx_enroll_student\", columnList = \"student_id\"),\n"
    "    @Index(name = \"idx_enroll_course\", columnList = \"course_id\")\n"
    "})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Enrollment {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n\n"
    "    @ManyToOne(fetch = FetchType.LAZY)\n"
    "    @JoinColumn(name = \"student_id\", nullable = false)\n"
    "    private Student student;\n\n"
    "    @ManyToOne(fetch = FetchType.LAZY)\n"
    "    @JoinColumn(name = \"course_id\", nullable = false)\n"
    "    private Course course;\n\n"
    "    @Column(nullable = false, length = 30)\n"
    "    private String status;\n\n"
    "    private LocalDateTime enrolledAt;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.entity.Enrollment;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n"
    "import java.util.Map;\n\n"
    "@Repository\n"
    "public class EnrollmentDaoImpl extends HibernatePaginationSortingDao<Long, Enrollment> {\n"
    "    public EnrollmentDaoImpl(EntityManager entityManager) {\n"
    "        super(Enrollment.class, entityManager);\n"
    "    }\n\n"
    "    public List<Enrollment> findByStudentId(Long studentId) {\n"
    "        return findByHql(\n"
    "            \"SELECT e FROM Enrollment e WHERE e.student.id = :studentId ORDER BY e.enrolledAt DESC\",\n"
    "            Map.of(\"studentId\", studentId)\n"
    "        );\n"
    "    }\n"
    "}\n"
    "```"
)

# ==============================================================================
# 5. XUẤT RA DATASET.JSONL MỚI
# ==============================================================================
output_file = os.path.join(script_dir, "dataset.jsonl")
with open(output_file, "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\n=======================================================")
print(f"XUẤT DỮ LIỆU MỚI THÀNH CÔNG: {len(dataset)} mẫu.")
print(f"File lưu tại: {output_file}")
print("=======================================================")
