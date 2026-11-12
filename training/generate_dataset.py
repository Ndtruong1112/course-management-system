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

    truncated_content = content[:4200]
    if len(content) > 4200:
        truncated_content += "\n// ... [Phần còn lại tiếp tục theo cùng kiến trúc] ..."

    add_sample(
        system_role,
        f"Hãy cung cấp mã nguồn và giải thích các thành phần kỹ thuật chính trong file `{filename}` (`{rel_path}`).",
        f"Dưới đây là mã nguồn của `{filename}` trong hệ thống:\n\n"
        f"```java\n{truncated_content}\n```\n\n"
        f"**Phân tích kỹ thuật của {clean_name}:**\n"
        f"- Nằm trong package: `{os.path.dirname(rel_path)}`.\n"
        f"- Tuân thủ Java 21, Spring Boot 3, Jakarta Persistence và kiến trúc Hibernate Generic DAO của dự án."
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
    "Viết Module Quản lý Ghi danh (Enrollment) gồm Enrollment Entity, IEnrollmentDao và EnrollmentDaoImpl kế thừa HibernatePaginationSortingDao",
    "Dưới đây là mã nguồn chuẩn `com.mkii.coursemanagementsystem` cho Module **Enrollment**:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n"
    "import java.time.LocalDateTime;\n\n"
    "@Entity\n"
    "@Table(name = \"enrollments\", uniqueConstraints = {\n"
    "    @UniqueConstraint(name = \"uk_enrollment_student_course\", columnNames = {\"student_id\", \"course_id\"})\n"
    "}, indexes = {\n"
    "    @Index(name = \"idx_enrollment_student\", columnList = \"student_id\"),\n"
    "    @Index(name = \"idx_enrollment_course\", columnList = \"course_id\")\n"
    "})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "@EqualsAndHashCode(onlyExplicitlyIncluded = true)\n"
    "public class Enrollment {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    @EqualsAndHashCode.Include\n"
    "    private Long id;\n\n"
    "    @ManyToOne(fetch = FetchType.EAGER, optional = false)\n"
    "    @JoinColumn(name = \"student_id\", nullable = false)\n"
    "    private Student student;\n\n"
    "    @ManyToOne(fetch = FetchType.EAGER, optional = false)\n"
    "    @JoinColumn(name = \"course_id\", nullable = false)\n"
    "    private Course course;\n\n"
    "    @Column(nullable = false, length = 20)\n"
    "    private String status;\n\n"
    "    @Column(name = \"progress_percent\", nullable = false)\n"
    "    private Integer progressPercent;\n\n"
    "    @Column(name = \"enrolled_at\", nullable = false)\n"
    "    private LocalDateTime enrolledAt;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Enrollment;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class EnrollmentDaoImpl extends HibernatePaginationSortingDao<Long, Enrollment> implements IEnrollmentDao {\n"
    "    public EnrollmentDaoImpl(EntityManager entityManager) {\n"
    "        super(Enrollment.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Enrollment> findByStudentId(Long studentId) {\n"
    "        String hql = \"SELECT e FROM Enrollment e WHERE e.student.id = :studentId ORDER BY e.enrolledAt DESC\";\n"
    "        return getEntityManager().createQuery(hql, Enrollment.class)\n"
    "                .setParameter(\"studentId\", studentId)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "**Điểm lưu ý:** Constructor của DAO Impl chỉ nhận `EntityManager` và gọi `super(Enrollment.class, entityManager);`, tuyệt đối không dùng `JpaRepository`."
)

# ==============================================================================
# 4B. BÀI TẬP PHƯƠNG THỨC HQL, RAG-GROUNDED CODEGEN & QUY CHUẨN CHUYÊN SÂU
# ==============================================================================
rag_sys = (
    "Bạn là Kiến trúc sư Phần mềm Cao cấp chuyên gia Spring Boot 3 và Java 21 cho dự án Course Management System (`com.mkii.coursemanagementsystem`).\n"
    "Nhiệm vụ của bạn là viết mã nguồn Java và giải thích kiến trúc tuân thủ 100% chuẩn mực của dự án:\n"
    "1. Entity JPA: Sử dụng Jakarta Persistence (@Entity, @Table, @Id, @GeneratedValue, Lombok @Getter, @Setter, @Builder).\n"
    "2. Tầng DAO: Kế thừa HibernatePaginationSortingDao<Pk, Entity> với constructor super(Entity.class, entityManager), dùng EntityManager / findByHql(), không dùng JpaRepository.\n"
    "3. Tầng Service & REST: Tách Interface/Impl, DTO Pattern (RequestDTO với Jakarta Validation, ResponseDTO), MinIO + Soft Delete + Versioning chuẩn."
)

# 1) Phương thức HQL cụ thể trong DAO (rèn cú pháp hoàn chỉnh, không cụt giữa constructor)
add_sample(
    rag_sys,
    "[YÊU CẦU]:\nViết phương thức tìm kiếm khóa học theo khoảng thời lượng `findByDurationRange(Integer minDuration, Integer maxDuration)` trong `CourseDaoImpl` sử dụng `EntityManager` và HQL.\n\n"
    "[TÀI LIỆU THAM KHẢO TỪ CODEBASE DỰ ÁN - BÁM SÁT PACKAGE, CLASS, FIELD THẬT]\n"
    "// File: src/main/java/com/mkii/coursemanagementsystem/dao/impl/CourseDaoImpl.java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "@Repository\n"
    "public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {\n"
    "    public CourseDaoImpl(EntityManager entityManager) {\n"
    "        super(Course.class, entityManager);\n"
    "    }\n}",
    "Dưới đây là phần cài đặt đầy đủ phương thức `findByDurationRange` trong `CourseDaoImpl` tuân thủ chuẩn Hibernate Generic DAO và `EntityManager`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.ICourseDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Course;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n\n"
    "import java.util.List;\n"
    "import java.util.Map;\n\n"
    "@Repository\n"
    "public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {\n\n"
    "    public CourseDaoImpl(EntityManager entityManager) {\n"
    "        super(Course.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Course> findByDurationRange(Integer minDuration, Integer maxDuration) {\n"
    "        String hql = \"SELECT c FROM Course c WHERE c.duration BETWEEN :minDuration AND :maxDuration ORDER BY c.duration ASC\";\n"
    "        return findByHql(\n"
    "                hql,\n"
    "                Map.of(\"minDuration\", minDuration, \"maxDuration\", maxDuration)\n"
    "        );\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "**Giải thích:** Sử dụng `super(Course.class, entityManager)` đúng chuẩn dự án, truyền câu truy vấn HQL có tham số `:minDuration`, `:maxDuration` qua `findByHql` (được `HibernateGenericDao` ủy quyền cho `EntityManager.createQuery`), không dùng `JpaRepository`."
)

add_sample(
    rag_sys,
    "[YÊU CẦU]:\nViết phương thức lọc lượt ghi danh theo trạng thái và tiến độ tối thiểu `findByStatusAndMinProgress(String status, Integer minProgress)` trong `EnrollmentDaoImpl` sử dụng `EntityManager` và HQL.",
    "Dưới đây là mã nguồn phương thức `findByStatusAndMinProgress` trong `EnrollmentDaoImpl`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Enrollment;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class EnrollmentDaoImpl extends HibernatePaginationSortingDao<Long, Enrollment> implements IEnrollmentDao {\n\n"
    "    public EnrollmentDaoImpl(EntityManager entityManager) {\n"
    "        super(Enrollment.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Enrollment> findByStatusAndMinProgress(String status, Integer minProgress) {\n"
    "        String hql = \"SELECT e FROM Enrollment e WHERE e.status = :status AND e.progressPercent >= :minProgress ORDER BY e.enrolledAt DESC\";\n"
    "        return getEntityManager().createQuery(hql, Enrollment.class)\n"
    "                .setParameter(\"status\", status)\n"
    "                .setParameter(\"minProgress\", minProgress)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

add_sample(
    rag_sys,
    "[YÊU CẦU]:\nViết phương thức truy vấn lọc khóa học theo mức giá tối đa và từ khóa tiêu đề `searchByTitleAndMaxPrice(String keyword, Double maxPrice)` trong `CourseDaoImpl` sử dụng `EntityManager` và HQL.",
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.entity.Course;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {\n\n"
    "    public CourseDaoImpl(EntityManager entityManager) {\n"
    "        super(Course.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Course> searchByTitleAndMaxPrice(String keyword, Double maxPrice) {\n"
    "        String hql = \"SELECT c FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%')) AND c.price <= :maxPrice ORDER BY c.price ASC\";\n"
    "        return getEntityManager().createQuery(hql, Course.class)\n"
    "                .setParameter(\"keyword\", keyword == null ? \"\" : keyword.trim())\n"
    "                .setParameter(\"maxPrice\", maxPrice)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

# 2) RAG-grounded DTO design (chống nhầm file DTO tham khảo thành code đã nộp)
add_sample(
    rag_sys,
    "[YÊU CẦU]:\nThiết kế lớp `AssignmentRequestDTO` với đầy đủ validation Jakarta (`@NotBlank`, `@NotNull`, `@Min`, `@Max`) và `AssignmentResponseDTO` để tách biệt tầng REST và Entity.\n\n"
    "[TÀI LIỆU THAM KHẢO TỪ CODEBASE DỰ ÁN - BÁM SÁT PACKAGE, CLASS, FIELD THẬT]\n"
    "// File: src/main/java/com/mkii/coursemanagementsystem/dto/CourseRequestDTO.java\n"
    "package com.mkii.coursemanagementsystem.dto;\n"
    "@Data @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class CourseRequestDTO { @NotBlank private String title; }",
    "Dưới đây là mã nguồn hoàn chỉnh cho `AssignmentRequestDTO` và `AssignmentResponseDTO` trong package `com.mkii.coursemanagementsystem.dto`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dto;\n\n"
    "import jakarta.validation.constraints.*;\n"
    "import lombok.*;\n\n"
    "@Data\n"
    "@NoArgsConstructor\n"
    "@AllArgsConstructor\n"
    "@Builder\n"
    "public class AssignmentRequestDTO {\n"
    "    @NotNull(message = \"courseId không được để trống\")\n"
    "    private Long courseId;\n\n"
    "    @NotBlank(message = \"Tiêu đề bài tập không được để trống\")\n"
    "    @Size(max = 200, message = \"Tiêu đề tối đa 200 ký tự\")\n"
    "    private String title;\n\n"
    "    @NotNull(message = \"Điểm tối đa không được để trống\")\n"
    "    @Min(value = 1, message = \"Điểm tối đa phải >= 1\")\n"
    "    @Max(value = 100, message = \"Điểm tối đa <= 100\")\n"
    "    private Integer maxScore;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dto;\n\n"
    "import lombok.*;\n\n"
    "@Data\n"
    "@NoArgsConstructor\n"
    "@AllArgsConstructor\n"
    "@Builder\n"
    "public class AssignmentResponseDTO {\n"
    "    private Long id;\n"
    "    private Long courseId;\n"
    "    private String title;\n"
    "    private Integer maxScore;\n"
    "}\n"
    "```"
)

# 3) RAG-grounded Soft Delete & Module Generation
add_sample(
    rag_sys,
    "[YÊU CẦU]:\nTriển khai cơ chế xóa mềm (Soft Delete) cho Department entity và DepartmentDaoImpl bằng cách cập nhật deleted=true thay vì xóa cứng khỏi cơ sở dữ liệu.\n\n"
    "[TÀI LIỆU THAM KHẢO TỪ CODEBASE DỰ ÁN - BÁM SÁT PACKAGE, CLASS, FIELD THẬT]\n"
    "// File: src/main/java/com/mkii/coursemanagementsystem/dao/impl/DepartmentDaoImpl.java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "@Repository\n"
    "public class DepartmentDaoImpl extends HibernatePaginationSortingDao<Long, Department> implements IDepartmentDao {\n"
    "    public DepartmentDaoImpl(EntityManager entityManager) {\n"
    "        super(Department.class, entityManager);\n"
    "    }\n"
    "}\n\n"
    "[HƯỚNG DẪN TRẢ LỜI]: Nếu yêu cầu bảo viết/thiết kế class hoặc phương thức, hãy xuất đầy đủ code Java hoàn chỉnh (gồm package, imports, annotations, class/method) chuẩn theo tài liệu tham khảo trên.",
    "Dưới đây là mã nguồn đầy đủ để nâng cấp cơ chế Xóa Mềm (**Soft Delete**) cho `Department` và `DepartmentDaoImpl` chuẩn kiến trúc `com.mkii.coursemanagementsystem`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n"
    "import org.hibernate.annotations.SQLDelete;\n"
    "import org.hibernate.annotations.Where;\n\n"
    "@Entity\n"
    "@Table(name = \"departments\")\n"
    "@SQLDelete(sql = \"UPDATE departments SET deleted = true WHERE id = ?\")\n"
    "@Where(clause = \"deleted = false\")\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Department {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n\n"
    "    @Column(nullable = false, unique = true, length = 100)\n"
    "    private String name;\n\n"
    "    @Builder.Default\n"
    "    @Column(nullable = false)\n"
    "    private Boolean deleted = false;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.IDepartmentDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Department;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n\n"
    "@Repository\n"
    "public class DepartmentDaoImpl extends HibernatePaginationSortingDao<Long, Department> implements IDepartmentDao {\n"
    "    public DepartmentDaoImpl(EntityManager entityManager) {\n"
    "        super(Department.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public void softDeleteById(Long id) {\n"
    "        String hql = \"UPDATE Department d SET d.deleted = true WHERE d.id = :id\";\n"
    "        getEntityManager().createQuery(hql)\n"
    "                .setParameter(\"id\", id)\n"
    "                .executeUpdate();\n"
    "    }\n\n"
    "    @Override\n"
    "    public void delete(Long id) {\n"
    "        deleteByPk(id);\n"
    "    }\n"
    "}\n"
    "```"
)

add_sample(
    rag_sys,
    "[YÊU CẦU]:\nTriển khai cơ chế xóa mềm (Soft Delete) cho Entity `Course` và `CourseDaoImpl` bằng cờ `deleted = true` kết hợp `@SQLDelete` và phương thức `deleteByPk`.",
    "Dưới đây là triển khai cơ chế Xóa Mềm (**Soft Delete**) chuẩn kiến trúc `com.mkii.coursemanagementsystem`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n"
    "import org.hibernate.annotations.SQLDelete;\n"
    "import org.hibernate.annotations.Where;\n\n"
    "@Entity\n"
    "@Table(name = \"courses\")\n"
    "@SQLDelete(sql = \"UPDATE courses SET deleted = true WHERE id = ?\")\n"
    "@Where(clause = \"deleted = false\")\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "public class Course {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    private Long id;\n\n"
    "    @Column(nullable = false, length = 255)\n"
    "    private String title;\n\n"
    "    @Builder.Default\n"
    "    @Column(nullable = false)\n"
    "    private Boolean deleted = false;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.ICourseDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Course;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n\n"
    "@Repository\n"
    "public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {\n"
    "    public CourseDaoImpl(EntityManager entityManager) {\n"
    "        super(Course.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public void softDeleteById(Long id) {\n"
    "        Course entity = get(id);\n"
    "        if (entity != null) {\n"
    "            entity.setDeleted(true);\n"
    "            super.update(entity);\n"
    "        }\n"
    "    }\n\n"
    "    @Override\n"
    "    public void delete(Long id) {\n"
    "        deleteByPk(id);\n"
    "    }\n"
    "}\n"
    "```"
)

add_sample(
    rag_sys,
    "[YÊU CẦU]:\nTạo module Quản lý Phòng học (Classroom) gồm `Classroom` Entity và `ClassroomDaoImpl` theo đúng kiến trúc của Course Management System.",
    "Dưới đây là mã nguồn hoàn chỉnh cho Module `Classroom` theo chuẩn `com.mkii.coursemanagementsystem`:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.entity;\n\n"
    "import jakarta.persistence.*;\n"
    "import lombok.*;\n\n"
    "@Entity\n"
    "@Table(name = \"classrooms\", indexes = {\n"
    "    @Index(name = \"idx_classroom_code\", columnList = \"room_code\", unique = true)\n"
    "})\n"
    "@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder\n"
    "@EqualsAndHashCode(onlyExplicitlyIncluded = true)\n"
    "public class Classroom {\n"
    "    @Id\n"
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
    "    @EqualsAndHashCode.Include\n"
    "    private Long id;\n\n"
    "    @Column(name = \"room_code\", nullable = false, unique = true, length = 30)\n"
    "    private String roomCode;\n\n"
    "    @Column(nullable = false)\n"
    "    private Integer capacity;\n"
    "}\n"
    "```\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.IClassroomDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Classroom;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class ClassroomDaoImpl extends HibernatePaginationSortingDao<Long, Classroom> implements IClassroomDao {\n"
    "    public ClassroomDaoImpl(EntityManager entityManager) {\n"
    "        super(Classroom.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Classroom> findByMinCapacity(Integer minCapacity) {\n"
    "        String hql = \"SELECT r FROM Classroom r WHERE r.capacity >= :minCapacity ORDER BY r.capacity ASC\";\n"
    "        return getEntityManager().createQuery(hql, Classroom.class)\n"
    "                .setParameter(\"minCapacity\", minCapacity)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```"
)

# 4) Kiến trúc lưu trữ MinIO vs MySQL metadata, Versioning & Security
add_sample(
    rag_sys,
    "Giải thích chi tiết cách Course Management System phân tách nơi lưu file nhị phân vật lý và dữ liệu quản lý tài liệu (`Document`, `MinioStorageService`).",
    "Trong **Course Management System** (`com.mkii.coursemanagementsystem`):\n"
    "- **File nhị phân vật lý** (PDF, DOCX, XLSX, PNG, JPG) được tải lên và lưu trực tiếp trên **MinIO S3 Object Storage** thông qua `MinioStorageService` (bucket `minio.bucket-name`).\n"
    "- **Cơ sở dữ liệu quan hệ MySQL** (bảng `tbl_document` / `documents` ánh xạ bởi entity `Document`) lưu phần **metadata** quản lý gồm: `id`, `name`, `path` (object key trên MinIO), `appId` (cột khóa ngoại `APP_DETAIL_FK`), `version`, `active`, `deleted`, `owner`.\n"
    "- Khi xóa tài liệu, hệ thống thực hiện **xóa mềm** (`deleted = true`, `active = false`) thay vì xóa cứng bản ghi."
)

add_sample(
    rag_sys,
    "Trong `DocumentServiceImpl`, quy trình đánh số phiên bản (versioning) hoạt động ra sao khi tải lên một tài liệu trùng tên trong cùng `appId`?",
    "Trong `DocumentServiceImpl.createDocument` và `createDocumentWithNewVersion`:\n"
    "1. Lần upload đầu tiên cho `(name, appId)`: tài liệu mới được tạo với `version = 1.0`, `active = true`, `deleted = false`.\n"
    "2. Khi upload trùng tên trong cùng `appId` (tìm thấy qua `documentDao.getDocumentName(originalFilename, appId)`):\n"
    "   - Bản ghi cũ bị vô hiệu hóa bằng `documentDetail.setActive(false)` và cập nhật qua `documentDao.update(documentDetail)`.\n"
    "   - Bản ghi mới giữ `active = true` và tăng số phiên bản lên **+ 1** (`Double versionCount = documentDetail.getVersion() != null ? documentDetail.getVersion() : 1.0; doc.setVersion(++versionCount);`), tức từ `1.0` lên `2.0`, `3.0`...\n"
    "3. Nếu quá trình lưu DB lỗi sau khi upload MinIO, `DocumentServiceImpl` thực hiện rollback bù trừ bằng `minioStorageService.delete(path)`."
)

add_sample(
    rag_sys,
    "Hệ thống sử dụng cơ chế bảo mật nào cho API và dữ liệu nhạy cảm của Sinh viên?",
    "Hệ thống áp dụng **2 lớp bảo mật**:\n"
    "1. **Spring Security + Stateless JWT (`SecurityConfig`, `JwtTokenProvider`, `JwtAuthenticationFilter`)**: Bảo vệ API theo vai trò (`ADMIN`, `TEACHER`, `LECTURER`, `USER`). Public các route `/api/auth/**`, `/api/dashboard/**`, GET `/api/courses/**`, GET `/api/departments/**`; các thao tác PII sinh viên, ghi danh (`/api/enrollments/**`), tài liệu (`/api/documents/**`) yêu cầu JWT hợp lệ.\n"
    "2. **Mã hóa AES-256 ở tầng JPA (`AesEncryptConverter`, `AESUtil`)**: Tự động mã hóa/giải mã dữ liệu nhạy cảm khi lưu xuống MySQL qua `AttributeConverter`."
)

add_sample(
    rag_sys,
    "Tóm tắt các quy chuẩn bắt buộc khi thiết kế một Module Entity + Generic DAO mới (ví dụ `Tutor` hoặc `Mentor`) trong dự án Course Management System.",
    "Khi bổ sung module mới vào `com.mkii.coursemanagementsystem`, mọi lớp phải tuân thủ 5 nguyên tắc:\n"
    "1. **Package gốc**: Entity đặt trong `com.mkii.coursemanagementsystem.entity`, DAO interface trong `com.mkii.coursemanagementsystem.dao`, DAO impl trong `com.mkii.coursemanagementsystem.dao.impl`.\n"
    "2. **Entity JPA + Lombok**: Dùng `jakarta.persistence.*` (`@Entity`, `@Table`, `@Id`, `@GeneratedValue(strategy = GenerationType.IDENTITY)`, `@Index`) và Lombok (`@Getter`, `@Setter`, `@NoArgsConstructor`, `@AllArgsConstructor`, `@Builder`). Hỗ trợ xóa mềm bằng `@SQLDelete`, `@Where(clause = \"deleted = false\")` và cờ `deleted = false`.\n"
    "3. **Generic DAO**: Interface `I<Name>Dao extends IPaginationSortingDao<Long, <Name>>`; lớp Impl kế thừa `HibernatePaginationSortingDao<Long, <Name>>` với constructor `public <Name>DaoImpl(EntityManager entityManager) { super(<Name>.class, entityManager); }`.\n"
    "4. **Truy vấn động**: Dùng `findByHql(...)` hoặc `getEntityManager().createQuery(...)` với named parameters (`:param`), không dùng `Spring Data JpaRepository`.\n"
    "5. **DTO Pattern**: Tách `RequestDTO` (có `@NotBlank`, `@NotNull`, `@Min`, `@Size`) và `ResponseDTO` trong `com.mkii.coursemanagementsystem.dto`."
)

# Scan Markdown reference docs (.agents/skills/cms-standards/references/*.md + README.md)
docs_to_learn = [os.path.join(base_dir, "README.md")]
refs_dir = os.path.join(base_dir, ".agents", "skills", "cms-standards", "references")
if os.path.isdir(refs_dir):
    for fn in sorted(os.listdir(refs_dir)):
        if fn.endswith(".md"):
            docs_to_learn.append(os.path.join(refs_dir, fn))

for md_path in docs_to_learn:
    if not os.path.exists(md_path):
        continue
    rel_md = os.path.relpath(md_path, base_dir).replace("\\", "/")
    try:
        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            md_text = f.read().strip()
        if md_text:
            add_sample(
                rag_sys,
                f"Tóm tắt các quy chuẩn kiến trúc và hướng dẫn kỹ thuật cốt lõi được định nghĩa trong `{rel_md}`.",
                md_text[:2800]
            )
    except Exception:
        pass

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
