# TOÀN BỘ MÃ NGUỒN DỰ ÁN COURSE MANAGEMENT SYSTEM

Tài liệu này tổng hợp toàn bộ các file Java, Generic DAO, MinIO Storage, JPA Specification và cấu hình để nạp vào Mô hình AI Lớn (Teacher Model) phục vụ Chưng cất Tri thức (Knowledge Distillation).

---

## File: `src/main/java/com/mkii/coursemanagementsystem/CourseManagementSystemApplication.java`

```java
package com.mkii.coursemanagementsystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CourseManagementSystemApplication {

    public static void main(String[] args) {
        SpringApplication.run(CourseManagementSystemApplication.class, args);
    }

}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/ApiConstants.java`

```java
package com.mkii.coursemanagementsystem.common;

public final class ApiConstants {

    private ApiConstants() {
        // Prevent instantiation
    }

    public static final String BASE_COURSE_URL = "/api/courses";
    public static final String BASE_STUDENT_URL = "/api/students";
    public static final String BASE_DOCUMENT_URL = "/api/documents";
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/MessageConstants.java`

```java
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
    public static final String STUDENT_NOT_FOUND = "Không tìm thấy sinh viên với ID: %d";
    public static final String DOCUMENT_NOT_FOUND = "Không tìm thấy tài liệu với ID: %s";
    public static final String FILE_EXTENSION_NOT_SUPPORTED = "Định dạng file không được hỗ trợ. Chỉ chấp nhận: PDF, XLSX, XLS, DOC, DOCX, JPG, JPEG, PNG";
    public static final String INVALID_DOCUMENT = "Tài liệu không tồn tại hoặc không hợp lệ.";
    public static final String SUCCESS_JSON = "{\"status\": \"SUCCESS\", \"message\": \"Thao tác thành công\"}";
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/BadRequestException.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

public class BadRequestException extends RuntimeException {

    public BadRequestException(String message) {
        super(message);
    }

    public BadRequestException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/ErrorResponse.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ErrorResponse {
    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/GlobalExceptionHandler.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import java.time.LocalDateTime;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException ex, HttpServletRequest request) {
        logger.warn("Resource not found: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.NOT_FOUND.value())
                .error(HttpStatus.NOT_FOUND.getReasonPhrase())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException ex, HttpServletRequest request) {
        String validationErrors = ex.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining("; "));
        logger.warn("Validation failed: {}", validationErrors);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(validationErrors)
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentTypeMismatchException.class)
    public ResponseEntity<ErrorResponse> handleTypeMismatchException(MethodArgumentTypeMismatchException ex, HttpServletRequest request) {
        String message = String.format("Tham số '%s' có giá trị '%s' không đúng kiểu dữ liệu yêu cầu", ex.getName(), ex.getValue());
        logger.warn("Type mismatch: {}", message);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(message)
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadableException(HttpMessageNotReadableException ex, HttpServletRequest request) {
        logger.warn("Malformed JSON request: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message("Dữ liệu gửi lên không đúng định dạng JSON.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<ErrorResponse> handleDataIntegrityViolationException(DataIntegrityViolationException ex, HttpServletRequest request) {
        logger.warn("Data integrity violation: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.CONFLICT.value())
                .error(HttpStatus.CONFLICT.getReasonPhrase())
                .message("Dữ liệu vi phạm ràng buộc cơ sở dữ liệu (ví dụ: email đã tồn tại).")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.CONFLICT);
    }

    @ExceptionHandler({BadRequestException.class, IllegalArgumentException.class})
    public ResponseEntity<ErrorResponse> handleBadRequestException(Exception ex, HttpServletRequest request) {
        logger.warn("Bad request: {}", ex.getMessage());
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error(HttpStatus.BAD_REQUEST.getReasonPhrase())
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex, HttpServletRequest request) {
        logger.error("Internal server error: ", ex);
        ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error(HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase())
                .message(ex.getMessage() != null ? ex.getMessage() : "Đã xảy ra lỗi hệ thống.")
                .path(request.getRequestURI())
                .build();
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/common/exception/ResourceNotFoundException.java`

```java
package com.mkii.coursemanagementsystem.common.exception;

public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }

    public ResourceNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/config/MinioConfig.java`

```java
package com.mkii.coursemanagementsystem.config;

import io.minio.MinioClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MinioConfig {

    @Value("${minio.endpoint:http://localhost:9000}")
    private String endpoint;

    @Value("${minio.access-key:minioadmin}")
    private String accessKey;

    @Value("${minio.secret-key:minioadmin}")
    private String secretKey;

    @Bean
    public MinioClient minioClient() {
        return MinioClient.builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/ICourseDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Course;

import java.util.List;

public interface ICourseDao extends IPaginationSortingDao<Long, Course> {

    Course save(Course course);

    Course update(Course course);

    void delete(Long id);

    Course getById(Long id);

    Course getByTitle(String title);

    List<Course> getAll();

    List<Course> searchByTitle(String keyword);

    List<Course> findByPriceRange(Double minPrice, Double maxPrice);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IDocumentDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;

import java.util.List;

public interface IDocumentDao extends IPaginationSortingDao<String, Document> {

    Document save(Document document);

    Document update(Document document);

    void delete(String id);

    Document getById(String id);

    Document findByPk(String id);

    Document getDocumentName(String fileName, String appId);

    List<Document> getDocumentByAppId(String appId);

    List<Document> findByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IGenericDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Base Generic DAO interface defining standard CRUD and basic query operations.
 * Keeping this interface clean and focused purely on core entity persistence.
 */
public interface IGenericDao<Pk, Entity> {

    @Transactional
    Entity create(Entity anEntity);

    @Transactional
    Entity update(Entity anEntity);

    @Transactional
    Entity saveOrUpdate(Entity anEntity);

    @Transactional
    void delete(Entity anEntity);

    @Transactional
    void deleteById(Pk id);

    void deleteByPk(Pk id);

    Entity get(Pk id);

    Optional<Entity> findById(Pk id);

    Entity getByField(String fieldName, Object value);

    List<Entity> findByField(String fieldName, Object value);

    List<Entity> getAll();

    @Transactional
    List<Entity> createAll(List<Entity> entities);

    @Transactional
    void deleteAll(List<Entity> entities);

    boolean exists(Pk id);

    long count();

    void flush();

    void clear();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IPaginationSortingDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.List;

/**
 * Interface extending {@link IGenericDao} dedicated to Sorting, Pagination,
 * and Dynamic Specification Search.
 */
public interface IPaginationSortingDao<Pk, Entity> extends IGenericDao<Pk, Entity> {

    /** Get all records sorted by a field name and direction ("asc" / "desc"). */
    List<Entity> findAllSorted(String sortBy, String direction);

    /** Get a single page of records, sorted. */
    Page<Entity> findAllPaged(int page, int size, String sortBy, String direction);

    /** Find all records matching a field value, applying Sort. */
    List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort);

    /** Find all records matching a field value, sorted by string parameters. */
    List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction);

    /** Find all records matching a field value, with full Pageable (page + size + sort). */
    Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable);

    /** Find all records matching a field value with pagination and sorting via string parameters. */
    Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction);

    /** Search by query string (key:op:value) using Specification. */
    List<Entity> searchBySpecification(String search);

    /** Search by query string using Specification combined with sorting. */
    List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Search by query string using Specification combined with pagination and sorting. */
    Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    /** Raw Spring Data Specification search without paging. */
    List<Entity> findAll(Specification<Entity> spec);

    /** Raw Spring Data Specification search with paging. */
    Page<Entity> findAll(Specification<Entity> spec, Pageable pageable);

    /** Raw Spring Data Specification search with sort. */
    List<Entity> findAll(Specification<Entity> spec, Sort sort);

    Page<Entity> getAll(Pageable pageable);

    List<Entity> getAll(Sort sort);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/IStudentDao.java`

```java
package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Student;

import java.util.List;
import java.util.Optional;

public interface IStudentDao extends IPaginationSortingDao<Long, Student> {

    Student save(Student student);

    Student update(Student student);

    void delete(Long id);

    Student getById(Long id);

    Student getByEmail(String email);

    Optional<Student> findByEmail(String email);

    List<Student> getAll();

    List<Student> searchByKeyword(String keyword);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/CourseDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;

@Repository
public class CourseDaoImpl extends HibernatePaginationSortingDao<Long, Course> implements ICourseDao {

    private static final Logger logger = LoggerFactory.getLogger(CourseDaoImpl.class);

    public CourseDaoImpl(EntityManager entityManager) {
        super(Course.class, entityManager);
    }

    @Override
    public Course save(Course course) {
        logger.info("Saving Course: {}", course.getTitle());
        return create(course);
    }

    @Override
    public Course update(Course course) {
        logger.info("Updating Course: {}", course.getId());
        return super.update(course);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Course: {}", id);
        deleteByPk(id);
    }

    @Override
    public Course getById(Long id) {
        logger.info("Getting Course by id: {}", id);
        return get(id);
    }

    @Override
    public Course getByTitle(String title) {
        logger.info("Getting Course by title: {}", title);
        return getByField("title", title);
    }

    @Override
    public List<Course> getAll() {
        logger.info("Getting all Courses");
        return findAll(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "id"));
    }

    @Override
    public List<Course> searchByTitle(String keyword) {
        logger.info("Searching Courses by title keyword: {}", keyword);
        return findByHql(
                "SELECT c FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%'))",
                java.util.Map.of("keyword", keyword)
        );
    }

    @Override
    public List<Course> findByPriceRange(Double minPrice, Double maxPrice) {
        logger.info("Getting Courses by price range: {} - {}", minPrice, maxPrice);
        return findByHql(
                "SELECT c FROM Course c WHERE c.price BETWEEN :minPrice AND :maxPrice",
                java.util.Map.of("minPrice", minPrice, "maxPrice", maxPrice)
        );
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Course count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/DocumentDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class DocumentDaoImpl extends HibernatePaginationSortingDao<String, Document> implements IDocumentDao {

    private static final Logger logger = LoggerFactory.getLogger(DocumentDaoImpl.class);

    public DocumentDaoImpl(EntityManager entityManager) {
        super(Document.class, entityManager);
    }

    @Override
    public Document save(Document document) {
        logger.info("Saving Document: name={}, appId={}", document.getName(), document.getAppId());
        return create(document);
    }

    @Override
    public Document update(Document document) {
        logger.info("Updating Document: id={}", document.getId());
        return super.update(document);
    }

    @Override
    public void delete(String id) {
        logger.info("Deleting Document: id={}", id);
        deleteByPk(id);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting Document by id: {}", id);
        return get(id);
    }

    @Override
    public Document findByPk(String id) {
        logger.info("Finding Document by pk: {}", id);
        return get(id);
    }

    @Override
    public Document getDocumentName(String fileName, String appId) {
        logger.info("document name: {} for appId: {}", fileName, appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByName", Document.class)
                    .setParameter("name", fileName)
                    .setParameter("appId", appId);
            List<Document> list = query.setMaxResults(1).getResultList();
            return list.isEmpty() ? null : list.get(0);
        } catch (Exception e) {
            logger.error("Error executing getDocumentByName: {}", e.getMessage());
            return null;
        }
    }

    @Override
    public List<Document> getDocumentByAppId(String appId) {
        logger.info("Inside getDocumentByAppId appId: {}", appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByAppId", Document.class)
                    .setParameter("appId", appId);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error executing getDocumentByAppId: {}", e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public List<Document> findByAppId(String appId) {
        return getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active Documents");
        return findByHql(
                "SELECT d FROM Document d WHERE d.deleted = false ORDER BY d.creationTime DESC",
                null
        );
    }

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);

        int offset = (lowerLimit != null && lowerLimit >= 0) ? lowerLimit : 0;
        int limit = (upperLimit != null && upperLimit > 0) ? upperLimit : 10;
        String sortField = (orderBy != null && !orderBy.isBlank()) ? orderBy : "creationTime";
        String direction = (orderType != null && !orderType.isBlank()) ? orderType : "desc";

        StringBuilder jpql = new StringBuilder("SELECT d FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        Sort sort = buildSort(sortField, direction);
        jpql.append(buildOrderClause(sort));

        TypedQuery<Document> typedQuery = getEntityManager().createQuery(jpql.toString(), Document.class);
        params.forEach(typedQuery::setParameter);
        typedQuery.setFirstResult(offset);
        typedQuery.setMaxResults(limit);

        return typedQuery.getResultList();
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("getDocCount: query={}, appId={}", query, appId);

        StringBuilder jpql = new StringBuilder("SELECT COUNT(d) FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        TypedQuery<Long> countQuery = getEntityManager().createQuery(jpql.toString(), Long.class);
        params.forEach(countQuery::setParameter);

        Long count = countQuery.getSingleResult();
        return count != null ? count.intValue() : 0;
    }

    @Override
    public Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("findByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        return findByFieldPaged("appId", appId, page, size, sortBy, direction);
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dao/impl/StudentDaoImpl.java`

```java
package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Repository
public class StudentDaoImpl extends HibernatePaginationSortingDao<Long, Student> implements IStudentDao {

    private static final Logger logger = LoggerFactory.getLogger(StudentDaoImpl.class);

    public StudentDaoImpl(EntityManager entityManager) {
        super(Student.class, entityManager);
    }

    @Override
    public Student save(Student student) {
        logger.info("Saving Student: {}", student.getFullName());
        return create(student);
    }

    @Override
    public Student update(Student student) {
        logger.info("Updating Student: {}", student.getId());
        return super.update(student);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        deleteByPk(id);
    }

    @Override
    public Student getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        return get(id);
    }

    @Override
    public Student getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        return getByField("email", email);
    }

    @Override
    public Optional<Student> findByEmail(String email) {
        logger.info("Getting Student optional by email: {}", email);
        return Optional.ofNullable(getByField("email", email));
    }

    @Override
    public List<Student> getAll() {
        logger.info("Getting all Students");
        return findAll(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "id"));
    }

    @Override
    public List<Student> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return findByHql(
                "SELECT s FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :keyword, '%'))",
                java.util.Map.of("keyword", keyword)
        );
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return (int) count();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/CourseRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseRequestDTO {

    @NotBlank(message = "Tiêu đề khóa học không được để trống")
    @Size(max = 255, message = "Tiêu đề khóa học không được vượt quá 255 ký tự")
    private String title;

    private String description;

    @NotNull(message = "Thời lượng khóa học không được để trống")
    @PositiveOrZero(message = "Thời lượng khóa học phải lớn hơn hoặc bằng 0")
    private Integer duration;

    @NotNull(message = "Học phí khóa học không được để trống")
    @PositiveOrZero(message = "Học phí khóa học phải lớn hơn hoặc bằng 0")
    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/CourseResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseResponseDTO {
    private Long id;
    private String title;
    private String description;
    private Integer duration;
    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/StudentRequestDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentRequestDTO {

    @NotBlank(message = "Họ và tên không được để trống")
    @Size(max = 150, message = "Họ và tên không được vượt quá 150 ký tự")
    private String fullName;

    @NotBlank(message = "Email không được để trống")
    @Email(message = "Email không đúng định dạng")
    @Size(max = 150, message = "Email không được vượt quá 150 ký tự")
    private String email;

    @Pattern(regexp = "^$|[0-9]{10,11}", message = "Số điện thoại phải từ 10-11 chữ số")
    private String phone;

    @Size(max = 255, message = "Địa chỉ không được vượt quá 255 ký tự")
    private String address;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/dto/StudentResponseDTO.java`

```java
package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentResponseDTO {
    private Long id;
    private String fullName;
    private String email;
    private String phone;
    private String address;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Course.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "courses", indexes = {
        @Index(name = "idx_course_title", columnList = "title"),
        @Index(name = "idx_course_price", columnList = "price")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    private Integer duration;

    private Double price;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Document.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;
import java.util.UUID;

@NamedQuery(
        name = "getDocumentByName",
        query = "SELECT d FROM Document d WHERE d.name = :name AND d.deleted = false AND d.active = true AND d.appId = :appId"
)
@NamedQuery(
        name = "getDocumentByAppId",
        query = "SELECT d FROM Document d WHERE d.appId = :appId AND d.deleted = false ORDER BY d.creationTime DESC"
)
@Entity
@Table(name = "documents", indexes = {
        @Index(name = "idx_doc_app_id", columnList = "APP_DETAIL_FK"),
        @Index(name = "idx_doc_name", columnList = "NAME"),
        @Index(name = "idx_doc_deleted", columnList = "DELETED"),
        @Index(name = "idx_doc_active", columnList = "ACTIVE")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "ID", updatable = false, nullable = false, length = 36)
    @EqualsAndHashCode.Include
    private String id;

    @Column(name = "APP_DETAIL_FK", nullable = false)
    private String appId;

    @Column(name = "NAME")
    private String name;

    @Column(name = "PATH")
    private String path;

    @Column(name = "OWNER")
    private String owner;

    @Column(name = "VERSION")
    private Double version;

    @Column(name = "DELETED")
    private Boolean deleted;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "CREATED_TIME")
    private Date creationTime;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "MODIFIED_TIME")
    private Date modificationTime;

    @Column(name = "ACTIVE")
    private Boolean active;

    @PrePersist
    void onCreate() {
        if (this.id == null || this.id.isBlank()) {
            this.id = UUID.randomUUID().toString();
        }
        Date now = new Date();
        this.creationTime = now;
        this.modificationTime = now;
        if (this.deleted == null) {
            this.deleted = false;
        }
        if (this.active == null) {
            this.active = true;
        }
        if (this.version == null) {
            this.version = 1.0;
        }
    }

    @PreUpdate
    void onPersist() {
        this.modificationTime = new Date();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/entity/Student.java`

```java
package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "students", indexes = {
        @Index(name = "idx_student_email", columnList = "email"),
        @Index(name = "idx_student_fullname", columnList = "fullName")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 150)
    private String fullName;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    @Column(length = 20)
    private String phone;

    @Column(length = 255)
    private String address;
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/hibernateDao/HibernateGenericDao.java`

```java
package com.mkii.coursemanagementsystem.hibernateDao;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.dao.IGenericDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.Query;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.jpa.repository.support.SimpleJpaRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Base Hibernate Generic DAO providing standard CRUD and basic JPQL operations.
 * Kept concise and clean. Advanced Pagination & Sorting has been separated into
 * {@link HibernatePaginationSortingDao}.
 */
public class HibernateGenericDao<Pk, Entity> extends SimpleJpaRepository<Entity, Pk> implements IGenericDao<Pk, Entity> {

    private static final Logger logger = LoggerFactory.getLogger(HibernateGenericDao.class);

    private Class<Entity> type;
    private EntityManager entityManager;

    public HibernateGenericDao(Class<Entity> type, EntityManager entityManager) {
        super(type, entityManager);
        this.type = type;
        this.entityManager = entityManager;
    }

    public Class<Entity> getType() {
        return type;
    }

    public void setType(Class<Entity> type) {
        this.type = type;
    }

    public EntityManager getEntityManager() {
        return entityManager;
    }

    public void setEntityManager(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    // ──────────── CRUD Operations ────────────

    @Override
    @Transactional
    public Entity create(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_CREATE_NULL_ENTITY, getType().getName()));
        }
        return save(anEntity);
    }

    @Override
    @Transactional
    public Entity update(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_UPDATE_NULL_ENTITY, getType().getName()));
        }
        return saveAndFlush(anEntity);
    }

    @Override
    @Transactional
    public Entity saveOrUpdate(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_SAVE_OR_UPDATE_NULL_ENTITY, getType().getName()));
        }
        return save(anEntity);
    }

    @Override
    @Transactional
    public void delete(Entity anEntity) {
        if (anEntity == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_DELETE_NULL_ENTITY, getType().getName()));
        }
        super.delete(anEntity);
    }

    @Override
    @Transactional
    public void deleteById(Pk id) {
        if (id == null) {
            logger.warn(MessageConstants.ENTITY_CANNOT_BE_NULL);
            throw new IllegalArgumentException(String.format(MessageConstants.CANNOT_DELETE_NULL_ID, getType().getName()));
        }
        super.deleteById(id);
    }

    @Override
    @Transactional
    public void deleteByPk(Pk id) {
        deleteById(id);
    }

    // ──────────── Basic Queries ────────────

    @Override
    public Entity get(Pk id) {
        if (id == null) {
            return null;
        }
        return super.findById(id).orElse(null);
    }

    @Override
    public Optional<Entity> findById(Pk id) {
        if (id == null) {
            return Optional.empty();
        }
        return super.findById(id);
    }

    @Override
    public Entity getByField(String fieldName, Object value) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return null;
        }
        logger.info("Getting {} by field: {} = {}", getType().getSimpleName(), fieldName, value);
        try {
            String jpql = "SELECT e FROM " + getType().getSimpleName() + " e WHERE e." + fieldName + " = :value";
            TypedQuery<Entity> query = entityManager.createQuery(jpql, getType());
            query.setParameter("value", value);
            List<Entity> results = query.setMaxResults(1).getResultList();
            return results.isEmpty() ? null : results.get(0);
        } catch (Exception e) {
            logger.error("Error getting {} by field {}: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return null;
        }
    }

    @Override
    public List<Entity> findByField(String fieldName, Object value) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return Collections.emptyList();
        }
        logger.info("Finding {} list by field: {} = {}", getType().getSimpleName(), fieldName, value);
        try {
            String jpql = "SELECT e FROM " + getType().getSimpleName() + " e WHERE e." + fieldName + " = :value";
            TypedQuery<Entity> query = entityManager.createQuery(jpql, getType());
            query.setParameter("value", value);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error finding {} by field {}: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return Collections.emptyList();
        }
    }

    protected boolean isValidIdentifier(String identifier) {
        return identifier != null && identifier.matches("^[a-zA-Z0-9_]+$");
    }

    @Override
    public List<Entity> getAll() {
        return findAll();
    }

    @Override
    @Transactional
    public List<Entity> createAll(List<Entity> entities) {
        if (entities == null || entities.isEmpty()) {
            return Collections.emptyList();
        }
        return saveAll(entities);
    }

    @Override
    @Transactional
    public void deleteAll(List<Entity> entities) {
        if (entities == null || entities.isEmpty()) {
            return;
        }
        super.deleteAll(entities);
    }

    // ──────────── Utility ────────────

    @Override
    public boolean exists(Pk id) {
        if (id == null) {
            return false;
        }
        return existsById(id);
    }

    @Override
    public long count() {
        return super.count();
    }

    @Override
    public void flush() {
        super.flush();
    }

    @Override
    public void clear() {
        if (entityManager != null) {
            entityManager.clear();
        }
    }

    // ──────────── JPQL / HQL Helper Methods ────────────

    public List<Entity> findByHql(String hql, Map<String, Object> params) {
        TypedQuery<Entity> query = entityManager.createQuery(hql, getType());
        if (params != null) {
            params.forEach(query::setParameter);
        }
        return query.getResultList();
    }

    @Transactional
    public int executeHql(String hql, Map<String, Object> params) {
        Query query = entityManager.createQuery(hql);
        if (params != null) {
            params.forEach(query::setParameter);
        }
        return query.executeUpdate();
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/hibernateDao/HibernatePaginationSortingDao.java`

```java
package com.mkii.coursemanagementsystem.hibernateDao;

import com.mkii.coursemanagementsystem.dao.IPaginationSortingDao;
import com.mkii.coursemanagementsystem.specification.GenericSpecificationsBuilder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.Collections;
import java.util.List;

/**
 * Specialized DAO implementation extending {@link HibernateGenericDao} that houses
 * all Sorting, Pagination, and Specification-based query logic.
 * Keeps HibernateGenericDao lean and modular.
 */
public class HibernatePaginationSortingDao<Pk, Entity> extends HibernateGenericDao<Pk, Entity> implements IPaginationSortingDao<Pk, Entity> {

    private static final Logger logger = LoggerFactory.getLogger(HibernatePaginationSortingDao.class);

    public HibernatePaginationSortingDao(Class<Entity> type, EntityManager entityManager) {
        super(type, entityManager);
    }

    // ──────────── Sorting / Pagination Methods ────────────

    @Override
    public List<Entity> findAllSorted(String sortBy, String direction) {
        logger.info("Finding all {} sorted by {} {}", getType().getSimpleName(), sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        return findAll(sort);
    }

    @Override
    public Page<Entity> findAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Finding all {} paged: page={}, size={}, sort={} {}", getType().getSimpleName(), page, size, sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        Pageable pageable = PageRequest.of(page, size, sort);
        return findAll(pageable);
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return Collections.emptyList();
        }
        logger.info("Finding {} by field {} = {} with sort {}", getType().getSimpleName(), fieldName, value, sort);
        try {
            String orderClause = buildOrderClause(sort);
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            TypedQuery<Entity> query = getEntityManager().createQuery(jpql, getType());
            query.setParameter("value", value);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error finding {} by field {} sorted: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
        logger.info("Finding {} by field {} = {} paged: page={}, size={}", getType().getSimpleName(), fieldName, value, pageable.getPageNumber(), pageable.getPageSize());
        try {
            // Count query
            String countJpql = "SELECT COUNT(e) FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value";
            Long total = getEntityManager().createQuery(countJpql, Long.class)
                    .setParameter("value", value)
                    .getSingleResult();

            if (total == null || total == 0) {
                return new PageImpl<>(Collections.emptyList(), pageable, 0);
            }

            // Data query with order and pagination
            String orderClause = buildOrderClause(pageable.getSort());
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            List<Entity> content = getEntityManager().createQuery(jpql, getType())
                    .setParameter("value", value)
                    .setFirstResult((int) pageable.getOffset())
                    .setMaxResults(pageable.getPageSize())
                    .getResultList();

            return new PageImpl<>(content, pageable, total);
        } catch (Exception e) {
            logger.error("Error finding {} by field {} paged: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction) {
        return findByFieldSorted(fieldName, value, buildSort(sortBy, direction));
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction) {
        Pageable pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return findByFieldPaged(fieldName, value, pageable);
    }

    // ──────────── Specification Search Methods ────────────

    @Override
    public List<Entity> searchBySpecification(String search) {
        logger.info("Searching {} by Specification query: {}", getType().getSimpleName(), search);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        return (spec == null) ? getAll() : findAll(spec);
    }

    @Override
    public List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching {} by spec sorted: search={}, sort={} {}", getType().getSimpleName(), search, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        Sort sort = buildSort(sortBy, direction);
        return (spec == null) ? findAllSorted(sortBy, direction) : findAll(spec, sort);
    }

    @Override
    public Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching {} by spec paged: search={}, page={}, size={}, sort={} {}", getType().getSimpleName(), search, page, size, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        PageRequest pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return (spec == null) ? getAll(pageable) : findAll(spec, pageable);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec, Sort sort) {
        return super.findAll(spec, sort);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec) {
        return super.findAll(spec);
    }

    @Override
    public Page<Entity> findAll(Specification<Entity> spec, Pageable pageable) {
        return super.findAll(spec, pageable);
    }

    @Override
    public Page<Entity> getAll(Pageable pageable) {
        return findAll(pageable);
    }

    @Override
    public List<Entity> getAll(Sort sort) {
        return findAll(sort);
    }

    // ──────────── Helper Methods ────────────

    protected Sort buildSort(String sortBy, String direction) {
        if (sortBy == null || sortBy.isBlank() || !isValidIdentifier(sortBy)) {
            return Sort.unsorted();
        }
        return "desc".equalsIgnoreCase(direction)
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
    }

    protected String buildOrderClause(Sort sort) {
        if (sort == null || sort.isUnsorted()) {
            return "";
        }
        StringBuilder sb = new StringBuilder(" ORDER BY ");
        boolean hasOrder = false;
        for (Sort.Order order : sort) {
            if (isValidIdentifier(order.getProperty())) {
                sb.append("e.")
                        .append(order.getProperty())
                        .append(" ")
                        .append(order.getDirection().name())
                        .append(", ");
                hasOrder = true;
            }
        }
        return hasOrder ? sb.substring(0, sb.length() - 2) : "";
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/repository/CourseRepository.java`

```java
package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CourseRepository extends JpaRepository<Course, Long>, JpaSpecificationExecutor<Course> {

    // Query 1: Tìm kiếm khóa học theo tên (Search title gần đúng) và map thẳng ra DTO
    @Query("SELECT new com.mkii.coursemanagementsystem.dto.CourseResponseDTO(c.id, c.title, c.description, c.duration, c.price) " +
            "FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<CourseResponseDTO> searchByTitle(@Param("keyword") String keyword);

    // Query 2: Lọc danh sách khóa học theo khoảng giá (Price range)
    @Query("SELECT new com.mkii.coursemanagementsystem.dto.CourseResponseDTO(c.id, c.title, c.description, c.duration, c.price) " +
            "FROM Course c WHERE c.price BETWEEN :minPrice AND :maxPrice")
    List<CourseResponseDTO> findByPriceRange(@Param("minPrice") Double minPrice, @Param("maxPrice") Double maxPrice);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/repository/DocumentRepository.java`

```java
package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DocumentRepository extends JpaRepository<Document, String>, JpaSpecificationExecutor<Document> {

    List<Document> findByAppIdAndDeletedFalse(String appId);

    List<Document> findByDeletedFalse();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/repository/StudentRepository.java`

```java
package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long>, JpaSpecificationExecutor<Student> {

    Optional<Student> findByEmail(String email);

    @Query("SELECT new com.mkii.coursemanagementsystem.dto.StudentResponseDTO(s.id, s.fullName, s.email, s.phone, s.address) " +
            "FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<StudentResponseDTO> searchByKeyword(@Param("keyword") String keyword);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/CourseRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface CourseRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Course> createCourse(@jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Course> updateCourse(@PathVariable Long id, @jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteCourse(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<CourseResponseDTO> getCourseById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<CourseResponseDTO>> getAllCourses();

    @GetMapping(value = {"/title/{title}", "/by-title"})
    ResponseEntity<CourseResponseDTO> getCourseByTitle(
            @PathVariable(required = false) String title,
            @RequestParam(required = false) String queryTitle);

    @PostMapping("/batch")
    ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(@RequestBody List<CourseRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<CourseResponseDTO> getCourseByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<CourseResponseDTO>> searchCourses(@RequestParam String keyword);

    @GetMapping("/filter")
    ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(
            @RequestParam Double minPrice,
            @RequestParam Double maxPrice);

    @GetMapping("/spec-search")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/courses/sorted?sortBy=title&direction=asc
     * Returns all courses sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/paged?page=0&size=10&sortBy=price&direction=desc
     * Returns a page of courses with metadata (totalElements, totalPages, …).
     */
    @GetMapping("/paged")
    ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-sorted?search=price>100&sortBy=price&direction=asc
     * Specification filter + sort, returns flat list.
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-paged?search=price>100&page=0&size=5&sortBy=price&direction=asc
     * Specification filter + pagination + sort.
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getCourseCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/DocumentRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentRest {

    @PostMapping(value = {"/create", "/upload", ""}, consumes = "multipart/form-data")
    ResponseEntity<List<Document>> createDocument(
            @RequestParam("files") List<MultipartFile> files,
            @RequestParam("appId") String appId);

    @GetMapping("/download")
    ResponseEntity<byte[]> downloadDocumentByPath(@RequestParam("filePath") String filePath);

    @GetMapping("/download/{id}")
    ResponseEntity<byte[]> downloadDocumentById(@PathVariable String id);

    @PostMapping("/delete")
    ResponseEntity<String> deleteDocument(@RequestBody Map<String, String> id);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteDocumentById(@PathVariable String id);

    @GetMapping("/{id}")
    ResponseEntity<Document> getDocumentById(@PathVariable String id);

    @GetMapping("/app/{appId}")
    ResponseEntity<List<Document>> getDocumentsByAppId(@PathVariable String appId);

    @GetMapping("/app/{appId}/paged")
    ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(
            @PathVariable String appId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping(value = {"/list", ""})
    ResponseEntity<List<Document>> getAllActiveDocuments();

    @GetMapping("/paged")
    ResponseEntity<Page<Document>> getDocumentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/sorted")
    ResponseEntity<List<Document>> getDocumentsSorted(
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<Document>> searchDocuments(
            @RequestParam(required = false) String query,
            @RequestParam(required = false, defaultValue = "0") Integer lowerLimit,
            @RequestParam(required = false, defaultValue = "10") Integer upperLimit,
            @RequestParam(required = false, defaultValue = "creationTime") String orderBy,
            @RequestParam(required = false, defaultValue = "desc") String orderType,
            @RequestParam(required = false) String appId);

    @GetMapping("/count")
    ResponseEntity<Integer> getDocCount(
            @RequestParam(required = false) String query,
            @RequestParam(required = false) String appId);

    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<Document>> searchBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/StudentRest.java`

```java
package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface StudentRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Student> createStudent(@jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Student> updateStudent(@PathVariable Long id, @jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteStudent(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<StudentResponseDTO> getStudentById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<StudentResponseDTO>> getAllStudents();

    @GetMapping(value = {"/email/{email}", "/by-email"})
    ResponseEntity<StudentResponseDTO> getStudentByEmail(
            @PathVariable(required = false) String email,
            @RequestParam(required = false) String queryEmail);

    @PostMapping("/batch")
    ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(@RequestBody List<StudentRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<StudentResponseDTO> getStudentByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<StudentResponseDTO>> searchStudents(@RequestParam String keyword);

    @GetMapping("/spec-search")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/students/sorted?sortBy=fullName&direction=asc
     * Returns all students sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/paged?page=0&size=10&sortBy=fullName&direction=asc
     * Returns a page of students with metadata.
     */
    @GetMapping("/paged")
    ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-sorted?search=email:test@&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-paged?search=email:test@&page=0&size=5&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getStudentCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/CourseRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.rest.CourseRest;
import com.mkii.coursemanagementsystem.service.CourseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(ApiConstants.BASE_COURSE_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class CourseRestImpl implements CourseRest {

    private static final Logger logger = LoggerFactory.getLogger(CourseRestImpl.class);

    @Autowired
    private CourseService courseService;

    @Override
    public ResponseEntity<Course> createCourse(@jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Creating new Course: {}", requestDTO.getTitle());
            Course course = courseService.create(requestDTO);
            return new ResponseEntity<>(course, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Course> updateCourse(Long id, @jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Updating Course: {}", id);
            Course course = courseService.update(requestDTO, id);
            return ResponseEntity.ok(course);
        } catch (Exception e) {
            logger.error("Error updating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteCourse(Long id) {
        try {
            logger.info("Deleting Course: {}", id);
            courseService.delete(id);
            return ResponseEntity.ok("Course deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseById(Long id) {
        try {
            logger.info("Getting Course by id: {}", id);
            CourseResponseDTO responseDTO = courseService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCourses() {
        try {
            logger.info("Getting all Courses");
            List<CourseResponseDTO> list = courseService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByTitle(String title, String queryTitle) {
        try {
            String searchTitle = title != null ? title : queryTitle;
            logger.info("Getting Course by title: {}", searchTitle);
            CourseResponseDTO responseDTO = courseService.getByTitle(searchTitle);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by title: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(List<CourseRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
            List<CourseResponseDTO> result = courseService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByField(String field, String value) {
        try {
            logger.info("Getting Course by field: {} = {}", field, value);
            CourseResponseDTO responseDTO = courseService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(String field, String value) {
        try {
            logger.info("Getting Course list by field: {} = {}", field, value);
            List<CourseResponseDTO> list = courseService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Course list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Course page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCourses(String keyword) {
        try {
            logger.info("Searching Courses by keyword: {}", keyword);
            List<CourseResponseDTO> list = courseService.searchByTitle(keyword);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(Double minPrice, Double maxPrice) {
        try {
            logger.info("Filtering Courses by price: {} - {}", minPrice, maxPrice);
            List<CourseResponseDTO> list = courseService.filterByPrice(minPrice, maxPrice);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error filtering Courses by price: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(String search) {
        try {
            logger.info("Searching Courses by Specification: {}", search);
            List<CourseResponseDTO> list = courseService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
            List<CourseResponseDTO> list = courseService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec sorted: {}, {} {}", search, sortBy, direction);
            List<CourseResponseDTO> list = courseService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getCourseCount() {
        try {
            logger.info("Getting Course count");
            Integer count = courseService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Course count: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/DocumentRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.rest.DocumentRest;
import com.mkii.coursemanagementsystem.service.DocumentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(ApiConstants.BASE_DOCUMENT_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class DocumentRestImpl implements DocumentRest {

    private static final Logger logger = LoggerFactory.getLogger(DocumentRestImpl.class);

    @Autowired
    private DocumentService documentService;

    @Override
    public ResponseEntity<List<Document>> createDocument(List<MultipartFile> files, String appId) {
        try {
            logger.info("REST: Creating documents for appId: {}, total files: {}", appId, files != null ? files.size() : 0);
            List<Document> documents = documentService.create(files, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error creating documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentByPath(String filePath) {
        try {
            logger.info("REST: Downloading document by filePath: {}", filePath);
            return documentService.download(filePath);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by path: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentById(String id) {
        try {
            logger.info("REST: Downloading document by id: {}", id);
            return documentService.downloadById(id);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocument(Map<String, String> id) {
        try {
            logger.info("REST: Deleting document with request body: {}", id);
            String result = documentService.delete(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocumentById(String id) {
        try {
            logger.info("REST: Deleting document by id: {}", id);
            String result = documentService.deleteById(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Document> getDocumentById(String id) {
        try {
            logger.info("REST: Getting document by id: {}", id);
            Document document = documentService.getById(id);
            return ResponseEntity.ok(document);
        } catch (Exception e) {
            logger.error("REST: Error getting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsByAppId(String appId) {
        try {
            logger.info("REST: Getting documents for appId: {}", appId);
            List<Document> documents = documentService.getByAppId(appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents for appId: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents for appId: {} paged: page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
            Page<Document> documents = documentService.getByAppIdPaged(appId, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents by appId paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getAllActiveDocuments() {
        try {
            logger.info("REST: Getting all active documents");
            List<Document> documents = documentService.getAllActive();
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting all documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<Document> documents = documentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsSorted(String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents sorted: sort={} {}", sortBy, direction);
            List<Document> documents = documentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> searchDocuments(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        try {
            logger.info("REST: Searching documents: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                    query, lowerLimit, upperLimit, orderBy, orderType, appId);
            List<Document> documents = documentService.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getDocCount(String query, String appId) {
        try {
            logger.info("REST: Getting document count: query={}, appId={}", query, appId);
            Integer count = documentService.getDocCount(query, appId);
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("REST: Error getting document count: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Searching documents by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<Document> documents = documentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents by spec paged: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/rest/impl/StudentRestImpl.java`

```java
package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.rest.StudentRest;
import com.mkii.coursemanagementsystem.service.StudentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(ApiConstants.BASE_STUDENT_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class StudentRestImpl implements StudentRest {

    private static final Logger logger = LoggerFactory.getLogger(StudentRestImpl.class);

    @Autowired
    private StudentService studentService;

    @Override
    public ResponseEntity<Student> createStudent(@jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Creating new Student: {}", requestDTO.getFullName());
            Student student = studentService.create(requestDTO);
            return new ResponseEntity<>(student, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Student> updateStudent(Long id, @jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Updating Student: {}", id);
            Student student = studentService.update(requestDTO, id);
            return ResponseEntity.ok(student);
        } catch (Exception e) {
            logger.error("Error updating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteStudent(Long id) {
        try {
            logger.info("Deleting Student: {}", id);
            studentService.delete(id);
            return ResponseEntity.ok("Student deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentById(Long id) {
        try {
            logger.info("Getting Student by id: {}", id);
            StudentResponseDTO responseDTO = studentService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudents() {
        try {
            logger.info("Getting all Students");
            List<StudentResponseDTO> list = studentService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByEmail(String email, String queryEmail) {
        try {
            String searchEmail = email != null ? email : queryEmail;
            logger.info("Getting Student by email: {}", searchEmail);
            StudentResponseDTO responseDTO = studentService.getByEmail(searchEmail);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by email: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(List<StudentRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Students", requestDTOs != null ? requestDTOs.size() : 0);
            List<StudentResponseDTO> result = studentService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByField(String field, String value) {
        try {
            logger.info("Getting Student by field: {} = {}", field, value);
            StudentResponseDTO responseDTO = studentService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(String field, String value) {
        try {
            logger.info("Getting Student list by field: {} = {}", field, value);
            List<StudentResponseDTO> list = studentService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Student list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Student page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudents(String keyword) {
        try {
            logger.info("Searching Students by keyword: {}", keyword);
            List<StudentResponseDTO> list = studentService.searchByKeyword(keyword);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(String search) {
        try {
            logger.info("Searching Students by Specification: {}", search);
            List<StudentResponseDTO> list = studentService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Students sorted by {} {}", sortBy, direction);
            List<StudentResponseDTO> list = studentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec sorted: {}, {} {}", search, sortBy, direction);
            List<StudentResponseDTO> list = studentService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Students by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getStudentCount() {
        try {
            logger.info("Getting Student count");
            Integer count = studentService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Student count: ", e);
            throw e;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/CourseService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;

import java.util.List;

public interface CourseService {

    Course create(CourseRequestDTO requestDTO);

    Course update(CourseRequestDTO requestDTO, Long id);

    void delete(Long id);

    CourseResponseDTO getById(Long id);

    List<CourseResponseDTO> getAll();

    List<CourseResponseDTO> searchByTitle(String keyword);

    List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice);

    CourseResponseDTO getByTitle(String title);

    CourseResponseDTO getByField(String field, Object value);

    /** Find multiple courses matching a specific field value (returns list). */
    List<CourseResponseDTO> findByFieldList(String field, Object value);

    /** Find courses matching a field with pagination and sorting. */
    Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple courses at once. */
    List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs);

    List<CourseResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all courses sorted by a field ("title", "price", …) and direction ("asc"/"desc"). */
    List<CourseResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of courses, sorted. */
    Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/DocumentService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentService {

    List<Document> create(List<MultipartFile> files, String appId);

    Document createDocument(String fileName, String appId, String fileobj);

    Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail);

    ResponseEntity<byte[]> download(String filePath);

    ResponseEntity<byte[]> downloadById(String id);

    String delete(Map<String, String> id);

    String deleteById(String id);

    Document fetchAndValidateDocumentById(Map<String, String> id);

    Document getById(String id);

    List<Document> getByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> getAllPaged(int page, int size, String sortBy, String direction);

    List<Document> getAllSorted(String sortBy, String direction);

    Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction);

    Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/MinioStorageService.java`

```java
package com.mkii.coursemanagementsystem.service;

import io.minio.BucketExistsArgs;
import io.minio.GetObjectArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.InputStream;

@Service
public class MinioStorageService {

    private static final Logger logger = LoggerFactory.getLogger(MinioStorageService.class);

    @Autowired
    private MinioClient minioClient;

    @Value("${minio.bucket-name:documents}")
    private String bucketName;

    public void ensureBucketExists() {
        try {
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
            if (!exists) {
                logger.info("MinIO bucket '{}' does not exist. Creating bucket...", bucketName);
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
            }
        } catch (Exception e) {
            logger.error("Error verifying/creating MinIO bucket '{}': {}", bucketName, e.getMessage());
            throw new RuntimeException("Could not connect to MinIO storage: " + e.getMessage(), e);
        }
    }

    public void upload(String objectPath, InputStream inputStream, String contentType, long size) {
        ensureBucketExists();
        try {
            logger.info("Uploading object '{}' to MinIO bucket '{}' (size: {} bytes)", objectPath, bucketName, size);
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .stream(inputStream, size, -1)
                            .contentType(contentType != null ? contentType : "application/octet-stream")
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error uploading object '{}' to MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to upload file to MinIO: " + e.getMessage(), e);
        }
    }

    public byte[] download(String objectPath) {
        try {
            logger.info("Downloading object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            try (InputStream stream = minioClient.getObject(
                    GetObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build())) {
                return IOUtils.toByteArray(stream);
            }
        } catch (Exception e) {
            logger.error("Error downloading object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to download file from MinIO: " + e.getMessage(), e);
        }
    }

    public void delete(String objectPath) {
        try {
            logger.info("Removing object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            minioClient.removeObject(
                    RemoveObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error deleting object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to delete file from MinIO: " + e.getMessage(), e);
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/StudentService.java`

```java
package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;

import java.util.List;

public interface StudentService {

    Student create(StudentRequestDTO requestDTO);

    Student update(StudentRequestDTO requestDTO, Long id);

    void delete(Long id);

    StudentResponseDTO getById(Long id);

    List<StudentResponseDTO> getAll();

    List<StudentResponseDTO> searchByKeyword(String keyword);

    StudentResponseDTO getByEmail(String email);

    StudentResponseDTO getByField(String field, Object value);

    /** Find multiple students matching a specific field value (returns list). */
    List<StudentResponseDTO> findByFieldList(String field, Object value);

    /** Find students matching a field with pagination and sorting. */
    Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple students at once. */
    List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs);

    List<StudentResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all students sorted by a field ("fullName", "email", …) and direction ("asc"/"desc"). */
    List<StudentResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of students, sorted. */
    Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/CourseServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.service.CourseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class CourseServiceImpl implements CourseService {

    private static final Logger logger = LoggerFactory.getLogger(CourseServiceImpl.class);

    // Call ONLY ICourseDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private ICourseDao courseDao;

    @Override
    public Course create(CourseRequestDTO requestDTO) {
        logger.info("Creating Course: {}", requestDTO.getTitle());
        Course course = new Course();
        mapRequestToEntity(requestDTO, course);
        return courseDao.save(course);
    }

    @Override
    public Course update(CourseRequestDTO requestDTO, Long id) {
        logger.info("Updating Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        mapRequestToEntity(requestDTO, existing);
        return courseDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        courseDao.delete(id);
    }

    @Override
    public CourseResponseDTO getById(Long id) {
        logger.info("Getting Course by id: {}", id);
        Course course = courseDao.getById(id);
        if (course == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> getAll() {
        logger.info("Getting all Courses");
        return courseDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> searchByTitle(String keyword) {
        logger.info("Searching Courses by title: {}", keyword);
        return courseDao.searchByTitle(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice) {
        logger.info("Filtering Courses by price range: {} - {}", minPrice, maxPrice);
        return courseDao.findByPriceRange(minPrice, maxPrice)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public CourseResponseDTO getByTitle(String title) {
        logger.info("Getting Course by title: {}", title);
        Course course = courseDao.getByTitle(title);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với tiêu đề: " + title);
        }
        return mapToDTO(course);
    }

    @Override
    public CourseResponseDTO getByField(String field, Object value) {
        logger.info("Getting Course by field: {} = {}", field, value);
        Course course = courseDao.getByField(field, value);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với " + field + ": " + value);
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Course list by field: {} = {}", field, value);
        return courseDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return courseDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Course> entities = requestDTOs.stream().map(dto -> {
            Course course = new Course();
            mapRequestToEntity(dto, course);
            return course;
        }).collect(Collectors.toList());
        return courseDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to ICourseDao) ────────────

    @Override
    public List<CourseResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Courses by Specification query: {}", search);
        return courseDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
        return courseDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return courseDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Courses by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return courseDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Courses by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return courseDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Course count");
        return courseDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(CourseRequestDTO requestDTO, Course course) {
        if (requestDTO.getTitle() != null) {
            course.setTitle(requestDTO.getTitle());
        }
        if (requestDTO.getDescription() != null) {
            course.setDescription(requestDTO.getDescription());
        }
        if (requestDTO.getDuration() != null) {
            course.setDuration(requestDTO.getDuration());
        }
        if (requestDTO.getPrice() != null) {
            course.setPrice(requestDTO.getPrice());
        }
    }

    private CourseResponseDTO mapToDTO(Course course) {
        return new CourseResponseDTO(
                course.getId(),
                course.getTitle(),
                course.getDescription(),
                course.getDuration(),
                course.getPrice()
        );
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/DocumentServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.service.DocumentService;
import com.mkii.coursemanagementsystem.service.MinioStorageService;
import org.apache.commons.io.FilenameUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
@Transactional
public class DocumentServiceImpl implements DocumentService {

    private static final Logger logger = LoggerFactory.getLogger(DocumentServiceImpl.class);

    private static final String[] SUPPORTED_EXTENSIONS = {
            "pdf", "xlsx", "xls", "doc", "docx", "jpg", "jpeg", "png"
    };

    // Strict architectural compliance: call ONLY IDocumentDao interface
    @Autowired
    private IDocumentDao documentDao;

    @Autowired
    private MinioStorageService minioStorageService;

    @Override
    @Transactional
    public List<Document> create(List<MultipartFile> files, String appId) {
        logger.info("Starting document creation for appId: {}, total files: {}", appId, files != null ? files.size() : 0);

        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId (mã công việc/nghiệp vụ) không được để trống.");
        }
        if (files == null || files.isEmpty()) {
            throw new BadRequestException("Danh sách file tải lên không hợp lệ hoặc để trống.");
        }

        List<Document> documentList = new ArrayList<>();

        for (MultipartFile file : files) {
            if (file != null && !file.isEmpty() && file.getOriginalFilename() != null && !file.getOriginalFilename().trim().isEmpty()) {
                String originalFilename = FilenameUtils.getName(file.getOriginalFilename());

                // 1. Kiểm tra ký tự đặc biệt trong tên file
                if (!checkFileNameSpecialChar(originalFilename)) {
                    throw new BadRequestException("Tên file không được chứa ký tự đặc biệt: " + originalFilename);
                }

                // 2. Kiểm tra độ dài tên file (phần trước dấu chấm <= 50 ký tự)
                String baseName = FilenameUtils.getBaseName(originalFilename);
                if (baseName.length() > 50) {
                    throw new BadRequestException("Tên file vượt quá độ dài tối đa 50 ký tự: " + baseName);
                }

                // 3. Kiểm tra định dạng đuôi file
                InputStream inputStream = validateFileExtension(file);

                String extension = FilenameUtils.getExtension(originalFilename);
                String storagePath = appId + "/" + UUID.randomUUID() + (extension.isEmpty() ? "" : "." + extension);

                // 4. Lưu trữ file lên MinIO
                minioStorageService.upload(storagePath, inputStream, file.getContentType(), file.getSize());

                // 5. Kiểm tra tài liệu cùng tên đã tồn tại cho appId này chưa (Versioning logic)
                Document documentDetail = documentDao.getDocumentName(originalFilename, appId);
                if (documentDetail == null) {
                    Document docData = createDocument(originalFilename, appId, storagePath);
                    documentList.add(docData);
                } else {
                    logger.info("Tài liệu '{}' đã tồn tại, tạo phiên bản mới", documentDetail.getName());
                    Document docDataWithNewVersion = createDocumentWithNewVersion(originalFilename, appId, storagePath, documentDetail);
                    documentList.add(docDataWithNewVersion);
                }
            } else {
                throw new BadRequestException("File tải lên không được để trống.");
            }
        }

        return documentList;
    }

    @Override
    public Document createDocument(String fileName, String appId, String fileobj) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);
        doc.setVersion(1.0);
        return documentDao.save(doc);
    }

    @Override
    public Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);

        // Vô hiệu hóa phiên bản cũ
        if (Boolean.TRUE.equals(documentDetail.getActive())) {
            documentDetail.setActive(false);
            documentDao.update(documentDetail);
        }

        // Tăng số phiên bản cho tài liệu mới
        Double versionCount = documentDetail.getVersion() != null ? documentDetail.getVersion() : 1.0;
        doc.setVersion(++versionCount);
        return documentDao.save(doc);
    }

    private void setDocumentDetails(String fileName, String appId, String fileobj, Document doc) {
        doc.setAppId(appId);
        doc.setName(fileName);
        doc.setPath(fileobj);
        doc.setOwner("SYSTEM");
        doc.setDeleted(false);
        doc.setActive(true);
    }

    public static boolean checkFileNameSpecialChar(String fileName) {
        if (fileName == null || fileName.isBlank()) {
            return false;
        }
        return fileName.matches("^[a-zA-Z0-9._\\s\\p{L}-]+$");
    }

    @Override
    public ResponseEntity<byte[]> download(String filePath) {
        logger.info("Downloading document by filePath: {}", filePath);
        if (filePath == null || filePath.trim().isEmpty()) {
            throw new BadRequestException("Đường dẫn file không được để trống.");
        }

        byte[] data = minioStorageService.download(filePath);
        String filename = FilenameUtils.getName(filePath);
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public ResponseEntity<byte[]> downloadById(String id) {
        logger.info("Downloading document by id: {}", id);
        Document document = getById(id);
        byte[] data = minioStorageService.download(document.getPath());

        String filename = document.getName() != null ? document.getName() : FilenameUtils.getName(document.getPath());
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public String delete(Map<String, String> id) {
        Document document = fetchAndValidateDocumentById(id);
        logger.info("Soft deleting document name: {}, id: {}", document.getName(), document.getId());
        document.setDeleted(true);
        document.setActive(false);
        documentDao.update(document);
        return MessageConstants.SUCCESS_JSON;
    }

    @Override
    public String deleteById(String id) {
        return delete(Map.of("id", id));
    }

    @Override
    public Document fetchAndValidateDocumentById(Map<String, String> id) {
        if (id == null) {
            throw new BadRequestException(MessageConstants.INVALID_DOCUMENT);
        }
        String docId = id.get("id");
        if (docId == null) {
            docId = id.get("ID");
        }
        if (docId != null && !docId.trim().isEmpty()) {
            Document document = documentDao.findByPk(docId.trim());
            if (document != null && !Boolean.TRUE.equals(document.getDeleted())) {
                return document;
            }
        }
        throw new ResourceNotFoundException(MessageConstants.INVALID_DOCUMENT);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting document by id: {}", id);
        Document document = documentDao.findByPk(id);
        if (document == null || Boolean.TRUE.equals(document.getDeleted())) {
            throw new ResourceNotFoundException(String.format(MessageConstants.DOCUMENT_NOT_FOUND, id));
        }
        return document;
    }

    @Override
    public List<Document> getByAppId(String appId) {
        logger.info("Getting documents for appId: {}", appId);
        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId không được để trống.");
        }
        return documentDao.getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active documents");
        return documentDao.getAllActive();
    }

    // ──────────── Pagination, Sorting & Search (Delegated to IDocumentDao) ────────────

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("Service getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);
        return documentDao.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("Service getDocCount: query={}, appId={}", query, appId);
        return documentDao.getDocCount(query, appId);
    }

    @Override
    public Page<Document> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Service getAllPaged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return documentDao.findAllPaged(page, size, sortBy, direction);
    }

    @Override
    public List<Document> getAllSorted(String sortBy, String direction) {
        logger.info("Service getAllSorted: sort={} {}", sortBy, direction);
        return documentDao.findAllSorted(sortBy, direction);
    }

    @Override
    public Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("Service getByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        return documentDao.findByAppIdPaged(appId, page, size, sortBy, direction);
    }

    @Override
    public Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Service searchBySpecificationPaged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return documentDao.searchBySpecificationPaged(search, page, size, sortBy, direction);
    }

    // ──────────── Private helper methods ────────────

    private InputStream validateFileExtension(MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null) {
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }

        String extension = FilenameUtils.getExtension(originalFilename).toLowerCase();
        logger.info("Validating extension from multipart: '{}'", extension);

        if (Arrays.asList(SUPPORTED_EXTENSIONS).contains(extension)) {
            try {
                return file.getInputStream();
            } catch (IOException e) {
                logger.error("Error reading file input stream: {}", e.getMessage(), e);
                throw new BadRequestException("Không thể đọc dữ liệu file: " + e.getMessage());
            }
        } else {
            logger.warn("File extension '{}' is not supported", extension);
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/service/impl/StudentServiceImpl.java`

```java
package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.StudentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class StudentServiceImpl implements StudentService {

    private static final Logger logger = LoggerFactory.getLogger(StudentServiceImpl.class);

    // Call ONLY IStudentDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private IStudentDao studentDao;

    @Override
    public Student create(StudentRequestDTO requestDTO) {
        logger.info("Creating Student: {}", requestDTO.getFullName());
        if (requestDTO.getEmail() != null) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        Student student = new Student();
        mapRequestToEntity(requestDTO, student);
        return studentDao.save(student);
    }

    @Override
    public Student update(StudentRequestDTO requestDTO, Long id) {
        logger.info("Updating Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        if (requestDTO.getEmail() != null && !requestDTO.getEmail().equalsIgnoreCase(existing.getEmail())) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null && !existingByEmail.getId().equals(id)) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        mapRequestToEntity(requestDTO, existing);
        return studentDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        studentDao.delete(id);
    }

    @Override
    public StudentResponseDTO getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        Student student = studentDao.getById(id);
        if (student == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> getAll() {
        logger.info("Getting all Students");
        return studentDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return studentDao.searchByKeyword(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public StudentResponseDTO getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        Student student = studentDao.getByEmail(email);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với email: " + email);
        }
        return mapToDTO(student);
    }

    @Override
    public StudentResponseDTO getByField(String field, Object value) {
        logger.info("Getting Student by field: {} = {}", field, value);
        Student student = studentDao.getByField(field, value);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với " + field + ": " + value);
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Student list by field: {} = {}", field, value);
        return studentDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return studentDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Students", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Student> entities = requestDTOs.stream().map(dto -> {
            Student student = new Student();
            mapRequestToEntity(dto, student);
            return student;
        }).collect(Collectors.toList());
        return studentDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to IStudentDao) ────────────

    @Override
    public List<StudentResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Students by Specification query: {}", search);
        return studentDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Students sorted by {} {}", sortBy, direction);
        return studentDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return studentDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Students by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return studentDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Students by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return studentDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return studentDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(StudentRequestDTO requestDTO, Student student) {
        if (requestDTO.getFullName() != null) {
            student.setFullName(requestDTO.getFullName());
        }
        if (requestDTO.getEmail() != null) {
            student.setEmail(requestDTO.getEmail());
        }
        if (requestDTO.getPhone() != null) {
            student.setPhone(requestDTO.getPhone());
        }
        if (requestDTO.getAddress() != null) {
            student.setAddress(requestDTO.getAddress());
        }
    }

    private StudentResponseDTO mapToDTO(Student student) {
        return new StudentResponseDTO(
                student.getId(),
                student.getFullName(),
                student.getEmail(),
                student.getPhone(),
                student.getAddress()
        );
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/GenericSpecification.java`

```java
package com.mkii.coursemanagementsystem.specification;

import jakarta.persistence.criteria.*;
import org.springframework.data.jpa.domain.Specification;

public class GenericSpecification<T> implements Specification<T> {

    private final SearchCriteria criteria;

    public GenericSpecification(SearchCriteria criteria) {
        this.criteria = criteria;
    }

    public SearchCriteria getCriteria() {
        return criteria;
    }

    @Override
    public Predicate toPredicate(Root<T> root, CriteriaQuery<?> query, CriteriaBuilder builder) {
        if (criteria == null || criteria.getKey() == null) {
            return null;
        }

        Path<?> path;
        try {
            path = root.get(criteria.getKey());
        } catch (IllegalArgumentException e) {
            return null; // Field does not exist on entity
        }

        String operation = criteria.getOperation();
        Object value = criteria.getValue();
        if (value == null) {
            return null;
        }

        String strValue = value.toString();
        Class<?> javaType = path.getJavaType();

        switch (operation) {
            case ">":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.gt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case ">=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.ge(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.greaterThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.lt(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThan(root.get(criteria.getKey()), strValue);
                }
                break;

            case "<=":
                if (Comparable.class.isAssignableFrom(javaType)) {
                    if (Number.class.isAssignableFrom(javaType)) {
                        Number num = parseNumber(javaType, strValue);
                        return num != null ? builder.le(root.get(criteria.getKey()), num) : null;
                    }
                    return builder.lessThanOrEqualTo(root.get(criteria.getKey()), strValue);
                }
                break;

            case "!":
            case "!=":
                if (javaType == String.class) {
                    return builder.notLike(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                }
                Object castVal = castToRequiredType(javaType, strValue);
                return castVal != null ? builder.notEqual(path, castVal) : null;

            case ":":
            default:
                if (javaType == String.class) {
                    return builder.like(builder.lower(root.get(criteria.getKey())), "%" + strValue.toLowerCase() + "%");
                } else {
                    Object eqVal = castToRequiredType(javaType, strValue);
                    return eqVal != null ? builder.equal(path, eqVal) : null;
                }
        }
        return null;
    }

    private Number parseNumber(Class<?> targetType, String str) {
        try {
            if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            }
            return Double.parseDouble(str);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private Object castToRequiredType(Class<?> targetType, String str) {
        try {
            if (targetType == String.class) {
                return str;
            } else if (targetType == Integer.class || targetType == int.class) {
                return Integer.parseInt(str);
            } else if (targetType == Long.class || targetType == long.class) {
                return Long.parseLong(str);
            } else if (targetType == Double.class || targetType == double.class) {
                return Double.parseDouble(str);
            } else if (targetType == Float.class || targetType == float.class) {
                return Float.parseFloat(str);
            } else if (targetType == Boolean.class || targetType == boolean.class) {
                return Boolean.parseBoolean(str);
            }
            return str;
        } catch (Exception e) {
            return null;
        }
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/GenericSpecificationsBuilder.java`

```java
package com.mkii.coursemanagementsystem.specification;

import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class GenericSpecificationsBuilder<T> {

    private final List<SearchCriteria> params = new ArrayList<>();

    public GenericSpecificationsBuilder<T> with(String key, String operation, Object value) {
        params.add(new SearchCriteria(key, operation, value));
        return this;
    }

    public GenericSpecificationsBuilder<T> with(SearchCriteria criteria) {
        params.add(criteria);
        return this;
    }

    public GenericSpecificationsBuilder<T> withSearchQuery(String search) {
        if (search == null || search.trim().isEmpty()) {
            return this;
        }
        // Match patterns: key>=val, key<=val, key!=val, key>val, key<val, key:val, key!val separated by comma
        Pattern pattern = Pattern.compile("([a-zA-Z0-9_.]+?)(>=|<=|!=|!|:|>|<)([a-zA-Z0-9_.@\\s\\p{L}-]+?)(?:,|$)");
        Matcher matcher = pattern.matcher(search);
        while (matcher.find()) {
            String key = matcher.group(1).trim();
            String op = matcher.group(2).trim();
            String value = matcher.group(3).trim();
            with(key, op, value);
        }
        return this;
    }

    public Specification<T> build() {
        if (params.isEmpty()) {
            return null;
        }

        Specification<T> result = new GenericSpecification<>(params.get(0));
        for (int i = 1; i < params.size(); i++) {
            result = Specification.where(result).and(new GenericSpecification<>(params.get(i)));
        }
        return result;
    }
}
```

---

## File: `src/main/java/com/mkii/coursemanagementsystem/specification/SearchCriteria.java`

```java
package com.mkii.coursemanagementsystem.specification;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SearchCriteria {
    private String key;
    private String operation;
    private Object value;
}
```

---

## File: `src/main/resources/application.properties`

```properties
spring.application.name=course-management-system

# Datasource Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/course_db?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=dmcvmkii28
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# HikariCP Connection Pool Optimization
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=30000
spring.datasource.hikari.connection-timeout=20000
spring.datasource.hikari.max-lifetime=1800000

# JPA & Hibernate Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.jpa.open-in-view=true

# Encoding Configuration
server.servlet.encoding.charset=UTF-8
server.servlet.encoding.enabled=true
server.servlet.encoding.force=true

# MinIO Object Storage Configuration
minio.endpoint=http://localhost:9000
minio.access-key=minioadmin
minio.secret-key=minioadmin
minio.bucket-name=documents

# Multipart File Upload Limits
spring.servlet.multipart.max-file-size=50MB
spring.servlet.multipart.max-request-size=100MB
```

---

