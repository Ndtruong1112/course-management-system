# Hệ thống Generic Hibernate DAO (DAO & Pagination Hierarchy)

Tài liệu này mô tả chi tiết cây kế thừa DAO, phân chia trách nhiệm giữa `HibernateGenericDao` và `HibernatePaginationSortingDao`, cùng các quy chuẩn kỹ thuật khi làm việc với tầng DAO.

---

## 1. Cây kế thừa tầng DAO

```text
                  IGenericDao<Pk, Entity>
                            ▲
                            │ extends
                IPaginationSortingDao<Pk, Entity>
                            ▲
                            │ extends
            ┌───────────────┴───────────────┐
            │                               │
    ICourseDao (Long)               IDocumentDao (String)
            ▲                               ▲
            │ implements                    │ implements
            │                               │
    CourseDaoImpl                   DocumentDaoImpl
            │ extends                       │ extends
            └───────────────┬───────────────┘
                            │
            HibernatePaginationSortingDao<Pk, Entity>
                            ▲
                            │ extends
                HibernateGenericDao<Pk, Entity>
                            ▲
                            │ extends
                SimpleJpaRepository<Entity, Pk>
```

---

## 2. Chi tiết các thành phần trong cây kế thừa

### 1. `IGenericDao<Pk, Entity>` & `HibernateGenericDao<Pk, Entity>`
* **Mục đích:** Cung cấp các thao tác CRUD nền tảng và JPQL/HQL Helpers. Được giữ gọn gàng, tinh gọn (lean), không bị phình to.
* **Các phương thức chính:**
  * `create(entity)`: Lưu mới thực thể (`save`).
  * `update(entity)`: Cập nhật và đồng bộ vào DB (`saveAndFlush`).
  * `delete(entity)` / `deleteById(id)` / `deleteByPk(id)`: Xóa thực thể.
  * `get(id)` / `findByPk(id)`: Lấy thực thể theo khóa chính (trả về null nếu không tồn tại).
  * `getByField(fieldName, value)`: Lấy duy nhất 1 bản ghi theo tên thuộc tính động. Bắt buộc có `isValidIdentifier(fieldName)` và `setMaxResults(1)` để tránh `NonUniqueResultException`.
  * `findByField(fieldName, value)`: Lấy danh sách bản ghi theo thuộc tính động.
  * `findByHql(hql, params)`: Thực thi câu lệnh HQL/JPQL tùy biến có tham số.
  * `executeHql(hql, params)`: Thực thi câu lệnh UPDATE / DELETE qua JPQL.

### 2. `IPaginationSortingDao<Pk, Entity>` & `HibernatePaginationSortingDao<Pk, Entity>`
* **Mục đích:** Tách biệt toàn bộ logic phân trang, sắp xếp và JPA Specification ra khỏi Generic CRUD cơ bản.
* **Các phương thức chính:**
  * `findAllSorted(sortBy, direction)`: Sắp xếp toàn bộ dữ liệu theo trường và chiều `asc`/`desc`.
  * `findAllPaged(page, size, sortBy, direction)`: Phân trang toàn bộ dữ liệu trả về đối tượng `Page<Entity>`.
  * `findByFieldPaged(fieldName, value, page, size, sortBy, direction)`: Phân trang dữ liệu lọc theo 1 thuộc tính cụ thể. Tự động kiểm tra `count` trước: nếu `count == 0` thì lập tức trả về trang rỗng (short-circuit) nhằm tiết kiệm tài nguyên truy vấn.
  * `searchBySpecificationPaged(searchQuery, page, size, sortBy, direction)`: Tìm kiếm đa tiêu chí bằng Specification kết hợp phân trang và sắp xếp.
  * `buildSort(sortBy, direction)`: Hàm helper tạo đối tượng `Sort` an toàn.
  * `buildOrderClause(sort)`: Hàm helper tạo chuỗi `ORDER BY e.property ASC/DESC` an toàn chống injection.

### 3. DAO cụ thể của từng Entity (`dao.impl.*`)
* Phải kế thừa `HibernatePaginationSortingDao<Pk, Entity>` và implement Interface DAO tương ứng.
* Constructor tiêm `EntityManager` và gọi `super(Entity.class, entityManager)`.
* **Ví dụ mẫu chuẩn cho Document:**
  ```java
  @Repository
  public class DocumentDaoImpl extends HibernatePaginationSortingDao<String, Document> implements IDocumentDao {
      private static final Logger logger = LoggerFactory.getLogger(DocumentDaoImpl.class);

      public DocumentDaoImpl(EntityManager entityManager) {
          super(Document.class, entityManager);
      }

      @Override
      public Document save(Document document) {
          return create(document);
      }

      @Override
      public Document update(Document document) {
          return super.update(document);
      }

      @Override
      public Document getDocumentName(String fileName, String appId) {
          TypedQuery<Document> query = getEntityManager()
                  .createNamedQuery("getDocumentByName", Document.class)
                  .setParameter("name", fileName)
                  .setParameter("appId", appId);
          List<Document> list = query.setMaxResults(1).getResultList();
          return list.isEmpty() ? null : list.get(0);
      }
      ...
  }
  ```

---

## 3. Cơ chế phòng chống JPQL Injection

Khi ghép tên trường vào câu lệnh truy vấn JPQL động (trong `getByField`, `findByField`, `findByFieldPaged`, `buildOrderClause`), bắt buộc phải kiểm tra thông qua hàm:

```java
protected boolean isValidIdentifier(String identifier) {
    return identifier != null && identifier.matches("^[a-zA-Z0-9_]+$");
}
```

Nếu tên trường chứa ký tự đặc biệt, dấu ngoặc, dấu chấm phẩy hoặc khoảng trắng bất thường, hệ thống sẽ ghi cảnh báo (warn log) và từ chối ghép trực tiếp vào truy vấn.
