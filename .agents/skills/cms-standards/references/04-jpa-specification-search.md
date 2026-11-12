# Cú pháp tìm kiếm JPA Specification (REST Query Search Language)

Tài liệu này hướng dẫn chi tiết về cấu trúc và cách sử dụng cơ chế tìm kiếm đa điều kiện dựa trên Spring Data JPA Specification (theo mẫu chuẩn Baeldung) được triển khai trong hệ thống.

---

## 1. Cấu trúc các thành phần

Bộ máy Specification Search bao gồm 3 lớp nằm trong package `com.mkii.coursemanagementsystem.specification`:

1. **`SearchCriteria`**: Đối tượng chứa 3 thông tin của một tiêu chí tìm kiếm:
   * `key` (String): Tên trường thuộc tính (ví dụ: `title`, `price`, `fullName`, `deleted`).
   * `operation` (String): Toán tử so sánh (`:`, `>`, `<`, `>=`, `<=`, `!`).
   * `value` (Object): Giá trị so sánh (tự động phân giải kiểu String, Số, Ngày tháng).
2. **`GenericSpecification<Entity>`**: Triển khai `Specification<Entity>` chuyển đổi `SearchCriteria` thành `jakarta.persistence.criteria.Predicate` thông qua `CriteriaBuilder`.
3. **`GenericSpecificationsBuilder<Entity>`**: Bộ phân tích cú pháp chuỗi query từ REST URL thành danh sách `SearchCriteria` và kết hợp chúng bằng phép toán `AND`.

---

## 2. Bảng toán tử hỗ trợ (Operators)

| Toán tử | Ý nghĩa | Ví dụ chuỗi truy vấn | Hành vi SQL / CriteriaBuilder |
| :---: | :--- | :--- | :--- |
| `:` | Bằng (Equality) hoặc Tìm gần đúng (LIKE) | `title:Java` | Nếu giá trị là chuỗi: `LIKE %Java%` (không phân biệt hoa thường). Nếu là số/boolean: so sánh bằng `=`. |
| `!` | Không bằng (Not Equal) | `status!INACTIVE` | Tạo điều kiện `NOT EQUAL` hoặc `NOT LIKE`. |
| `>` | Lớn hơn nghiêm ngặt (Strict Greater Than) | `price>500000` | Tạo điều kiện `greaterThan(root.get(key), value)`. |
| `<` | Nhỏ hơn nghiêm ngặt (Strict Less Than) | `duration<40` | Tạo điều kiện `lessThan(root.get(key), value)`. |
| `>=` | Lớn hơn hoặc bằng (Greater Than or Equal) | `price>=1000000` | Tạo điều kiện `greaterThanOrEqualTo(root.get(key), value)`. |
| `<=` | Nhỏ hơn hoặc bằng (Less Than or Equal) | `duration<=60` | Tạo điều kiện `lessThanOrEqualTo(root.get(key), value)`. |

> [!IMPORTANT]
> **Thứ tự ưu tiên trong biểu thức chính quy (Regex Precedence):**
> Trong `GenericSpecificationsBuilder`, mẫu regex bắt buộc phải đặt các toán tử 2 ký tự (`>=`, `<=`, `!=`) đứng trước các toán tử 1 ký tự (`>`, `<`, `!`, `:`) để tránh việc `price>=500` bị nhận diện nhầm thành toán tử `>` với giá trị `=500`.

---

## 3. Cú pháp kết hợp nhiều điều kiện (Multi-criteria Query)

Các điều kiện được phân tách bằng dấu phẩy `,`:

```text
GET /api/courses/spec-search?search=title:Spring,price>500000,duration<=60
```

Hệ thống sẽ:
1. Tách chuỗi thành 3 tiêu chí:
   * `title` LIKE `%Spring%`
   * `price` > `500000`
   * `duration` <= `60`
2. Kết hợp cả 3 bằng phép `AND`.

---

## 4. Tích hợp Phân trang và Sắp xếp nâng cao

Mọi Entity kế thừa `HibernatePaginationSortingDao` đều tự động có sẵn endpoint:
* `GET /api/{entity}/spec-search-sorted?search=...&sortBy=...&direction=...`
* `GET /api/{entity}/spec-search-paged?search=...&page=0&size=10&sortBy=...&direction=desc`

### Ví dụ truy vấn phân trang thực tế:
```http
GET /api/students/spec-search-paged?search=fullName:Nguyen,address:Hanoi&page=0&size=5&sortBy=fullName&direction=asc
```
Trả về đối tượng JSON dạng Spring Data Page:
```json
{
  "content": [ ... ],
  "pageable": { ... },
  "totalElements": 12,
  "totalPages": 3,
  "size": 5,
  "number": 0
}
```
