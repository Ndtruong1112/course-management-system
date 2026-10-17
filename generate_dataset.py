import os
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset = []

def add_sample(system_prompt, instruction, output):
    dataset.append({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": output}
        ]
    })

system_role = "Bạn là trợ lý AI chuyên gia, nắm vững 100% kiến trúc, mã nguồn và nghiệp vụ của dự án Course Management System (Hệ thống Quản lý Khóa học, Học viên & Tài liệu MinIO)."

# ==============================================================================
# 1. QUÉT CHỌN LỌC CÁC TỆP MÃ NGUỒN CHÍNH (LOẠI BỎ FILE RÁC & FILE QUÁ DÀI)
# ==============================================================================
ignore_dirs = {'.git', '.idea', '.mvn', 'target', '__pycache__', 'outputs'}
ignore_files = {
    'dataset.jsonl',
    'Course Management System - Full APIs.postman_collection.json',
    'pom.xml',
    'mvnw',
    'mvnw.cmd'
}

scanned_files = {}

for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file in ignore_files or file.endswith(('.py', '.jsonl')):
            continue
        if file.endswith(('.java', '.properties', '.sql', '.md')):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_dir).replace('\\', '/')
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Chỉ lấy các file có ý nghĩa kiến trúc
                    if len(content.strip()) > 0:
                        scanned_files[rel_path] = content
            except Exception:
                pass

print(f"-> Đã quét chọn lọc được {len(scanned_files)} tệp mã nguồn cốt lõi.")

# ==============================================================================
# 2. SINH CÂU HỎI - TRẢ LỜI ĐA DẠNG (PARAPHRASED) VỀ TỪNG TỆP MÃ NGUỒN
# ==============================================================================
for rel_path, content in scanned_files.items():
    filename = os.path.basename(rel_path)
    clean_name = os.path.splitext(filename)[0]

    # Cắt gọn nội dung code tối đa 2000 ký tự để không làm tràn cửa sổ context 1024 token
    truncated_content = content[:2200]
    if len(content) > 2200:
        truncated_content += "\n// ... [Nội dung mã nguồn được rút gọn để tối ưu hóa context] ..."

    # Mẫu 1: Vai trò và trách nhiệm trong kiến trúc
    add_sample(
        system_role,
        f"Lớp `{filename}` nằm ở đường dẫn `{rel_path}` đảm nhiệm vai trò gì trong kiến trúc Course Management System?",
        f"Trong kiến trúc dự án Course Management System, `{filename}` (`{rel_path}`) đóng vai trò quan trọng:\n\n"
        f"```java\n{truncated_content}\n```\n\n"
        f"File này chịu trách nhiệm cụ thể trong tầng kiến trúc tương ứng, đảm bảo tuân thủ thiết kế phân lớp và các nguyên lý của dự án."
    )

    # Mẫu 2: Diễn đạt tự nhiên khác (Paraphrase)
    add_sample(
        system_role,
        f"Hãy giải thích chi tiết cấu trúc và chức năng của `{clean_name}` trong dự án.",
        f"`{clean_name}` thuộc đường dẫn `{rel_path}`. Thành phần này được thiết kế như sau:\n\n"
        f"```java\n{truncated_content}\n```\n\n"
        f"Nó tương tác chặt chẽ với các thành phần khác trong hệ thống để xử lý nghiệp vụ theo chuẩn Enterprise."
    )

# ==============================================================================
# 3. SINH TRI THỨC NGHIỆP VỤ & KIẾN TRÚC CỐT LÕI (CHUYÊN SÂU)
# ==============================================================================

# A. Tổng quan & Package Structure
add_sample(
    system_role,
    "Dự án Course Management System gồm những module và package chính nào?",
    "Dự án Course Management System được xây dựng trên nền Spring Boot 3 / Java 21 với package gốc là `com.mkii.coursemanagementsystem` gồm 9 gói chức năng chính:\n"
    "1. `common`: Chứa hằng số API (`ApiConstants`), thông điệp hệ thống (`MessageConstants`), và xử lý ngoại lệ toàn cục (`GlobalExceptionHandler`, `ResourceNotFoundException`, `BadRequestException`).\n"
    "2. `config`: Cấu hình hệ thống, đặc biệt là `MinioConfig` kết nối đến MinIO S3 Object Storage.\n"
    "3. `entity`: Các thực thể JPA gồm `Course` (khóa học), `Student` (học viên), và `Document` (tài liệu đính kèm).\n"
    "4. `dto`: Data Transfer Objects gồm `CourseRequestDTO`, `CourseResponseDTO`, `StudentRequestDTO`, `StudentResponseDTO`.\n"
    "5. `hibernateDao` & `dao`: Kiến trúc Generic DAO pattern với `IGenericDao`, `IPaginationSortingDao`, `HibernateGenericDao`, `HibernatePaginationSortingDao` và các DAO cụ thể: `CourseDaoImpl`, `StudentDaoImpl`, `DocumentDaoImpl`.\n"
    "6. `repository`: Các interface Spring Data JPA repository: `CourseRepository`, `StudentRepository`, `DocumentRepository`.\n"
    "7. `service`: Tầng nghiệp vụ xử lý logic gồm `CourseService`, `StudentService`, `DocumentService`, `MinioStorageService` và các implementation tương ứng.\n"
    "8. `rest`: Tầng REST API controller giao tiếp với client gồm `CourseRest`, `StudentRest`, `DocumentRest` và các implementation tương ứng.\n"
    "9. `specification`: Hỗ trợ tìm kiếm động nhiều điều kiện qua JPA Specification: `GenericSpecification`, `GenericSpecificationsBuilder`, `SearchCriteria`."
)

# B. Kiến trúc Hibernate Generic DAO
add_sample(
    system_role,
    "Kiến trúc Hibernate Generic DAO trong Course Management System được tổ chức và hoạt động như thế nào?",
    "Hệ thống Generic DAO trong dự án được tổ chức phân cấp bài bản theo chuẩn Enterprise:\n"
    "1. `IGenericDao<Pk, Entity>`: Interface định nghĩa các thao tác CRUD cơ bản: `create`, `update`, `deleteByPk`, `get`, `findAll`, `count`, `findByField`.\n"
    "2. `IPaginationSortingDao<Pk, Entity>`: Interface mở rộng từ `IGenericDao`, bổ sung khả năng phân trang (`findAll(Pageable)`), sắp xếp (`findAll(Sort)`), và truy vấn tùy biến HQL (`findByHql`).\n"
    "3. `HibernateGenericDao<Pk, Entity>`: Lớp trừu tượng cài đặt `IGenericDao`, kế thừa từ `SimpleJpaRepository<Entity, Pk>` của Spring Data JPA và giữ tham chiếu tới `EntityManager`.\n"
    "4. `HibernatePaginationSortingDao<Pk, Entity>`: Kế thừa `HibernateGenericDao`, hiện thực hóa các phương thức phân trang, sắp xếp và HQL động qua `TypedQuery`.\n"
    "5. Các DAO nghiệp vụ (`CourseDaoImpl`, `StudentDaoImpl`, `DocumentDaoImpl`): Kế thừa `HibernatePaginationSortingDao` và bổ sung các hàm truy vấn đặc thù của từng thực thể."
)

add_sample(
    system_role,
    "Tại sao dự án Course Management System lại dùng kết hợp Generic DAO với Spring Data JPA?",
    "Dự án kết hợp cả hai mô hình để tận dụng thế mạnh tối đa:\n"
    "- `SimpleJpaRepository` của Spring Data JPA cung cấp sẵn sự ổn định và tối ưu bộ nhớ.\n"
    "- Lớp `HibernateGenericDao` và `HibernatePaginationSortingDao` bọc ngoài giúp lập trình viên viết các hàm dùng chung (Generic CRUD, HQL động, kiểm tra null tập trung, logging chuẩn hóa) mà không phải viết lặp lại ở từng Repository.\n"
    "- Giúp kiểm soát trực tiếp `EntityManager` khi cần thực thi các câu lệnh HQL phức tạp hoặc can thiệp sâu vào vòng đời của Hibernate Entity."
)

# C. Nghiệp vụ Thực thể & Truy vấn Mở rộng
add_sample(
    system_role,
    "Thực thể Course và CourseDaoImpl trong Course Management System được thiết kế như thế nào?",
    "Thực thể `Course` đại diện cho khóa học trong hệ thống:\n"
    "- Thuộc tính: `id` (Long, tự tăng), `title` (tiêu đề khóa học, độ dài 255, bắt buộc), `description` (TEXT), `duration` (thời lượng, Integer), `price` (học phí, Double).\n"
    "- Chỉ mục (Index) DB: `idx_course_title` trên cột `title`, `idx_course_price` trên cột `price` để tối ưu tốc độ tìm kiếm và sắp xếp.\n"
    "- Lớp `CourseDaoImpl` kế thừa `HibernatePaginationSortingDao<Long, Course>` và implement `ICourseDao`. Nó cung cấp các phương thức mở rộng:\n"
    "  + `searchByTitle(String keyword)`: Tìm kiếm không phân biệt hoa thường bằng HQL: `SELECT c FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%'))`.\n"
    "  + `findByPriceRange(Double minPrice, Double maxPrice)`: Lọc theo khoảng giá bằng HQL: `SELECT c FROM Course c WHERE c.price BETWEEN :minPrice AND :maxPrice`.\n"
    "  + `getByTitle(String title)`: Lấy khóa học theo tiêu đề chính xác.\n"
    "  + `getAll()`: Lấy toàn bộ danh sách sắp xếp giảm dần theo ID."
)

add_sample(
    system_role,
    "Thực thể Student và StudentDaoImpl được thiết kế như thế nào?",
    "Thực thể `Student` biểu diễn thông tin học viên:\n"
    "- Thuộc tính: `id` (Long, tự tăng), `fullName` (họ tên, bắt buộc, tối đa 150 ký tự), `email` (email duy nhất unique=true, bắt buộc, tối đa 150 ký tự), `phone` (số điện thoại, tối đa 20 ký tự), `address` (địa chỉ, tối đa 255 ký tự).\n"
    "- Chỉ mục DB: Unique index trên cột `email`, Index trên cột `fullName`.\n"
    "- Lớp `StudentDaoImpl` kế thừa `HibernatePaginationSortingDao<Long, Student>` và implement `IStudentDao`:\n"
    "  + `search(String keyword)`: Tìm kiếm học viên theo tên hoặc email bằng HQL: `SELECT s FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :kw, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :kw, '%'))`.\n"
    "  + `findByEmail(String email)`: Tra cứu chính xác học viên theo địa chỉ email."
)

# D. Nghiệp vụ Quản lý Tài liệu & MinIO Storage
add_sample(
    system_role,
    "Hệ thống quản lý tài liệu (Document Management) và MinIO trong Course Management System hoạt động như thế nào?",
    "Hệ thống quản lý tài liệu kết hợp giữa CSDL quan hệ và Object Storage phân tán:\n"
    "1. **MinIO Object Storage**: Lưu trữ file nhị phân vật lý (PDF, Word, Ảnh...) trong bucket riêng (mặc định tên bucket là `documents`).\n"
    "2. **MySQL Database**: Bảng `documents` chỉ lưu trữ metadata:\n"
    "   - `id`: Khóa chính định danh UUID 36 ký tự.\n"
    "   - `appId` (`APP_DETAIL_FK`): Khóa ngoại logic liên kết tài liệu với một khóa học hoặc một sinh viên cụ thể.\n"
    "   - `name`: Tên file gốc.\n"
    "   - `path`: Đường dẫn lưu trữ object trên MinIO bucket.\n"
    "   - `owner`: Tên người tải lên.\n"
    "   - `version`: Phiên bản của file (khởi tạo 1.0).\n"
    "   - `deleted`: Cờ xóa mềm (boolean, mặc định false).\n"
    "   - `active`: Cờ trạng thái hiệu lực (boolean, mặc định true)."
)

add_sample(
    system_role,
    "Giải thích cơ chế Nâng phiên bản (Versioning) khi upload file trùng tên trong DocumentServiceImpl.",
    "Trong `DocumentServiceImpl`, khi người dùng upload một file có tên trùng với file đã có trong cùng một hồ sơ (`appId`):\n"
    "1. Hệ thống gọi `documentDao.getDocumentName(fileName, appId)` để tra cứu bản ghi đang hoạt động (`active = true, deleted = false`).\n"
    "2. Nếu tìm thấy bản ghi cũ, hệ thống đặt `oldDoc.setActive(false)` và cập nhật lại bằng `documentDao.update(oldDoc)`.\n"
    "3. Bản ghi mới được gán phiên bản tăng thêm 1 đơn vị: `newDoc.setVersion(oldDoc.getVersion() + 1.0)` với `active = true`.\n"
    "4. Cả file cũ và file mới đều được lưu trên MinIO, giúp bảo toàn lịch sử thay đổi của tài liệu mà không bị ghi đè mất dữ liệu."
)

add_sample(
    system_role,
    "Giải thích cơ chế Xóa mềm (Soft Delete) trong DocumentServiceImpl.",
    "Trong phương thức `delete` của `DocumentServiceImpl`:\n"
    "- Hệ thống tra cứu tài liệu theo ID thông qua `documentDao.findByPk(docId)`.\n"
    "- Thay vì dùng lệnh `DELETE` xóa vĩnh viễn khỏi CSDL và MinIO, hệ thống chỉ cập nhật thuộc tính: `document.setDeleted(true)` và lưu lại qua `documentDao.update(document)`.\n"
    "- Lợi ích: Chống mất mát dữ liệu do lỡ tay xóa, phục vụ kiểm toán (audit log) và cho phép khôi phục dữ liệu khi cần."
)

# E. JPA Dynamic Specification & Criteria API
add_sample(
    system_role,
    "Cách dự án Course Management System triển khai tìm kiếm động bằng JPA Specification như thế nào?",
    "Dự án sử dụng Specification Pattern kết hợp Jakarta Persistence Criteria API:\n"
    "1. `SearchCriteria`: Lưu trữ điều kiện lọc gồm 3 thông tin: `key` (tên trường), `operation` (toán tử so sánh: `:`, `>`, `<`), và `value` (giá trị).\n"
    "2. `GenericSpecification<T>`: Implement interface `org.springframework.data.jpa.domain.Specification<T>`. Hàm `toPredicate(...)` tự động chuyển đổi `SearchCriteria` thành câu điều kiện SQL động:\n"
    "   - Toán tử `>`: `builder.greaterThanOrEqualTo(...)`\n"
    "   - Toán tử `<`: `builder.lessThanOrEqualTo(...)`\n"
    "   - Toán tử `:`: Với chuỗi thực hiện `LIKE %value%`, với kiểu khác thực hiện so sánh bằng `EQUAL`.\n"
    "3. `GenericSpecificationsBuilder<T>`: Thu thập danh sách các `SearchCriteria` và dùng `Specification.where().and(...)` để gộp nhiều điều kiện lại với nhau."
)

# ==============================================================================
# 4. BỔ SUNG CÁC MẪU CODE GENERATION (SINH MÃ NGUỒN MỚI CHUẨN KIẾN TRÚC DỰ ÁN)
# ==============================================================================

add_sample(
    system_role,
    "Hãy viết một lớp DAO mới tên là CategoryDaoImpl để quản lý Entity Category theo chuẩn kiến trúc Hibernate Generic DAO của dự án.",
    "Dưới đây là cài đặt `CategoryDaoImpl` tuân thủ 100% chuẩn kiến trúc của Course Management System:\n\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.dao.impl;\n\n"
    "import com.mkii.coursemanagementsystem.dao.ICategoryDao;\n"
    "import com.mkii.coursemanagementsystem.entity.Category;\n"
    "import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;\n"
    "import jakarta.persistence.EntityManager;\n"
    "import org.springframework.beans.factory.annotation.Autowired;\n"
    "import org.springframework.stereotype.Repository;\n"
    "import java.util.List;\n\n"
    "@Repository\n"
    "public class CategoryDaoImpl extends HibernatePaginationSortingDao<Long, Category> implements ICategoryDao {\n\n"
    "    @Autowired\n"
    "    public CategoryDaoImpl(EntityManager entityManager) {\n"
    "        super(Category.class, entityManager);\n"
    "    }\n\n"
    "    @Override\n"
    "    public List<Category> findByName(String name) {\n"
    "        String hql = \"SELECT c FROM Category c WHERE LOWER(c.name) LIKE LOWER(CONCAT('%', :name, '%'))\";\n"
    "        return getEntityManager().createQuery(hql, Category.class)\n"
    "                .setParameter(\"name\", name)\n"
    "                .getResultList();\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "Lớp trên kế thừa đầy đủ các phương thức CRUD, phân trang và sắp xếp từ `HibernatePaginationSortingDao` và tự quản lý `EntityManager` theo đúng chuẩn dự án."
)

add_sample(
    system_role,
    "Hãy viết phương thức tìm kiếm học viên theo số điện thoại trong StudentDaoImpl bằng HQL.",
    "Trong `StudentDaoImpl`, ta có thể bổ sung phương thức tìm kiếm học viên theo số điện thoại như sau:\n\n"
    "```java\n"
    "@Override\n"
    "public List<Student> findByPhone(String phone) {\n"
    "    String hql = \"SELECT s FROM Student s WHERE s.phone LIKE CONCAT('%', :phone, '%')\";\n"
    "    return getEntityManager().createQuery(hql, Student.class)\n"
    "            .setParameter(\"phone\", phone)\n"
    "            .getResultList();\n"
    "}\n"
    "```\n\n"
    "Phương thức này sử dụng `getEntityManager()` được cung cấp sẵn từ `HibernateGenericDao` để tạo `TypedQuery` an toàn kiểu dữ liệu."
)

add_sample(
    system_role,
    "Hãy hướng dẫn cách thêm một mã lỗi mới và xử lý ngoại lệ tùy chỉnh trong GlobalExceptionHandler của dự án.",
    "Để thêm và xử lý một ngoại lệ mới trong Course Management System:\n"
    "1. Khai báo chuỗi thông báo lỗi trong `MessageConstants`:\n"
    "```java\n"
    "public static final String FILE_FORMAT_NOT_SUPPORTED = \"Định dạng file không được hệ thống hỗ trợ.\";\n"
    "```\n"
    "2. Tạo ngoại lệ nghiệp vụ tùy chỉnh:\n"
    "```java\n"
    "package com.mkii.coursemanagementsystem.common.exception;\n"
    "public class UnsupportedFileTypeException extends RuntimeException {\n"
    "    public UnsupportedFileTypeException(String message) {\n"
    "        super(message);\n"
    "    }\n"
    "}\n"
    "```\n"
    "3. Khai báo handler xử lý tập trung trong `GlobalExceptionHandler`:\n"
    "```java\n"
    "@ExceptionHandler(UnsupportedFileTypeException.class)\n"
    "public ResponseEntity<ErrorResponse> handleUnsupportedFileTypeException(UnsupportedFileTypeException ex) {\n"
    "    ErrorResponse error = new ErrorResponse(HttpStatus.UNSUPPORTED_MEDIA_TYPE.value(), ex.getMessage(), System.currentTimeMillis());\n"
    "    return new ResponseEntity<>(error, HttpStatus.UNSUPPORTED_MEDIA_TYPE);\n"
    "}\n"
    "```"
)

# ==============================================================================
# 5. XUẤT RA FILE DATASET.JSONL
# ==============================================================================
output_file = os.path.join(base_dir, "dataset.jsonl")
with open(output_file, "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"\n=======================================================")
print(f"XUẤT DỮ LIỆU THÀNH CÔNG: {len(dataset)} mẫu câu hỏi - trả lời.")
print(f"File lưu tại: {output_file}")
print(f"=======================================================")
