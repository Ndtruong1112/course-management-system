# 04. Chuẩn mực Tầng Dữ liệu & Spring Data JPA

Tài liệu này cung cấp các hướng dẫn tối quan trọng cho tầng dữ liệu (Persistence Layer), thiết kế Entity chuẩn mực, kỹ thuật chống lỗi N+1 Query, kiểm soát giao dịch (`@Transactional`), và truy vấn động an toàn.

---

## 1. Lớp thực thể cơ sở chuẩn mực (`BaseAuditEntity`)

Mọi Entity chính trong hệ thống **bắt buộc kế thừa `BaseAuditEntity`** để tự động quản lý lịch sử bản ghi và hỗ trợ xóa mềm (Soft Delete):

```java
package com.company.project.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.ColumnDefault;
import org.springframework.data.annotation.CreatedBy;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedBy;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.io.Serializable;
import java.time.LocalDateTime;

@Getter
@Setter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseAuditEntity implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @CreatedDate
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(name = "created_by", updatable = false, length = 50)
    private String createdBy;

    @LastModifiedBy
    @Column(name = "updated_by", length = 50)
    private String updatedBy;

    @Column(name = "is_deleted", nullable = false)
    @ColumnDefault("false")
    private Boolean isDeleted = false;
}
```

*Kích hoạt JPA Auditing:* Cần thêm `@EnableJpaAuditing` tại một class cấu hình trong package `config`.

---

## 2. Quy chuẩn Thiết lập Quan hệ giữa các Entity (Relationships)

1. **BẮT BUỘC dùng `FetchType.LAZY` trên TẤT CẢ các mối quan hệ:**
   - Mặc định `@ManyToOne` và `@OneToOne` trong JPA là `EAGER` ➔ **Phải ghi đè thành `LAZY`**.
   - `FetchType.EAGER` là nguyên nhân hàng đầu làm chậm hệ thống và gây nghẽn RAM do tự động join toàn bộ cây dữ liệu.
   ```java
   // ĐÚNG
   @ManyToOne(fetch = FetchType.LAZY)
   @JoinColumn(name = "department_id", nullable = false)
   private Department department;

   // ĐÚNG
   @OneToMany(mappedBy = "course", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
   private List<Lesson> lessons = new ArrayList<>();
   ```
2. **Luôn khởi tạo Collection rỗng cho `@OneToMany`:** Tránh `NullPointerException` khi truy cập.
3. **Đánh chỉ mục (Index) trên Foreign Keys và các cột tìm kiếm:**
   ```java
   @Table(name = "courses", indexes = {
       @Index(name = "idx_courses_department_id", columnList = "department_id"),
       @Index(name = "idx_courses_title", columnList = "title"),
       @Index(name = "idx_courses_created_at", columnList = "created_at")
   })
   ```

---

## 3. Chiến lược triệt tiêu hoàn toàn lỗi N+1 Queries

### Lỗi N+1 là gì?
Khi load một danh sách $N$ bản ghi cha, hệ thống phát sinh thêm $N$ câu query phụ để load bản ghi con quan hệ Lazy. Tổng cộng phát sinh $1 + N$ queries làm DB quá tải.

### 2 Giải pháp chuẩn hóa:

#### Giải pháp 1: Sử dụng `@EntityGraph` trong Repository
```java
public interface CourseRepository extends JpaRepository<Course, Long> {

    @EntityGraph(attributePaths = {"department", "instructor"})
    List<Course> findAllByStatus(CourseStatus status);

    @EntityGraph(attributePaths = {"department", "instructor"})
    Optional<Course> findDetailById(Long id);
}
```

#### Giải pháp 2: Sử dụng `JOIN FETCH` trong câu `@Query`
```java
@Query("SELECT c FROM Course c JOIN FETCH c.department JOIN FETCH c.instructor WHERE c.id = :id")
Optional<Course> findWithDetailsById(@Param("id") Long id);
```

#### Quy tắc Production: Tắt Open-Session-In-View (OSIV)
Trong `application.yml`:
```yaml
spring:
  jpa:
    open-in-view: false # BẮT BUỘC: Ngăn Hibernate giữ DB Connection xuyên suốt qua Controller
```
*Lưu ý:* Khi OSIV tắt, nếu tầng Controller cố tình gọi getter của thuộc tính Lazy chưa được nạp sẵn, hệ thống sẽ ném `LazyInitializationException`. Điều này ép buộc lập trình viên phải chuẩn bị đầy đủ dữ liệu tại tầng Service thông qua DTO Mapper, đảm bảo hiệu năng tối đa.

---

## 4. Quản lý Giao dịch tường minh (`@Transactional`)

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true) // MẶC ĐỊNH CHO TOÀN BỘ CLASS: Tối ưu đọc, Hibernate không check dirty state
public class CourseServiceImpl implements CourseService {

    private final CourseRepository courseRepository;

    @Override
    public CourseResponse getById(Long id) {
        // Chạy với chế độ read-only
        return courseRepository.findById(id).map(CourseMapper::toResponse)...
    }

    @Override
    @Transactional // GHI ĐÈ CHO HÀM GHI/SỬA: Bắt đầu giao dịch ghi
    public CourseResponse create(CreateCourseRequest request) {
        Course course = CourseMapper.toEntity(request);
        Course saved = courseRepository.save(course);
        return CourseMapper.toResponse(saved);
    }
}
```
