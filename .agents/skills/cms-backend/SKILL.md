---
name: cms-backend
description: Implements and reviews Course Management System Java APIs using its Hibernate Generic DAO, service interfaces, DTOs, document storage, and authorization patterns. Use for backend changes in this repository.
---

# Backend CMS

## Nguồn cần đọc

Đọc `pom.xml` để xác định phiên bản; hiện cấu hình Java 21 và Spring Boot 4.1.1.
Không suy luận phiên bản từ SpringDoc hoặc README. Package gốc:
`com.mkii.coursemanagementsystem`.

Với một nghiệp vụ, đọc Entity, DTO, interface DAO/implementation,
interface Service/implementation, interface REST/implementation tương ứng.
`CourseDaoImpl`, `CourseServiceImpl`, `CourseRestImpl` là ví dụ hiện có,
không phải mẫu phải sao chép cả logging và lỗi lịch sử.

## Ràng buộc kiến trúc

- Service gọi interface DAO; không inject `EntityManager`, Generic DAO hoặc
  `SimpleJpaRepository` vào Service. Dùng constructor injection cho dependency mới.
- DAO nghiệp vụ kế thừa `HibernatePaginationSortingDao<Pk, Entity>` và
  implement interface DAO tương ứng; constructor truyền `Entity.class, entityManager`.
- Đọc chữ ký helper thật trước khi gọi. Code hiện có dùng `save`, `update`,
  `deleteByPk`, `get`, `findByHql`; không bịa `create()` từ quy chuẩn cũ.
- Giữ interface và `.impl` ở các tầng hiện có. Request DTO dùng Jakarta
  Validation; xác minh response contract trước khi đổi Entity thành DTO.
- HQL dùng parameter binding. Sort field/size có whitelist hoặc giới hạn phù
  hợp; UI danh sách dùng API phân trang, không tải toàn bộ để lọc ở trình duyệt.
- Thông báo nghiệp vụ/API mới tái sử dụng constants ở `common`; xử lý lỗi qua
  cơ chế hiện có, không nuốt exception hoặc trả thành công khi thất bại.

## Dữ liệu và quyền

Đọc `SecurityConfig` và endpoint thực tế trước khi thay đổi quyền. Đặc biệt
không mở `/api/students`, `/api/enrollments`, `/api/documents` chỉ để sửa lỗi UI.
Kiểm tra cả HEAD/download/delete và ownership nếu nghiệp vụ đòi hỏi.

Với document: đọc `DocumentServiceImpl`, DAO và MinIO service trước. Giữ mô hình
file binary ở MinIO, metadata ở DB, liên kết `APP_DETAIL_FK`, version/active và
xóa mềm theo code; xem bù trừ khi upload object thành công nhưng DB thất bại.
Không xem transaction DB là transaction của MinIO.

Không đổi khóa AES/JWT, seed demo hoặc schema khi chỉ sửa API/UI. Lỗi mã hóa
phải được báo, không chuyển sang lưu plaintext để "chạy được".

## Kiểm chứng

Chọn nhóm test liên quan trong `src/test/java/` theo phạm vi được cho phép.
Phân biệt test H2/mock với MySQL/MinIO thật. Không nâng dependency hoặc đổi
toàn bộ kiến trúc trong một bugfix. Chi tiết chuẩn nghiệp vụ bổ sung nằm trong
`../cms-standards/references/`; chỉ đọc reference cần cho tác vụ hiện tại.
