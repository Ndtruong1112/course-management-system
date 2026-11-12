# 06. Chuẩn mực Kiểm thử Tự động (Testing Standards)

Tài liệu này cung cấp các nguyên tắc xây dựng bộ kiểm thử tự động toàn diện, cấu trúc bài test chuẩn BDD, kỹ thuật cô lập phụ thuộc với Mockito, kiểm thử lát cắt (Slice Testing), và quy tắc kiểm thử theo yêu cầu (On-Demand Testing).

---

## 1. Kim tự tháp kiểm thử (Testing Pyramid)

```text
       /\
      /  \      10% End-to-End Tests (@SpringBootTest toàn bộ context, Testcontainers)
     /----\
    /      \    20% Slice Tests (@WebMvcTest cho Controller, @DataJpaTest cho Repository)
   /--------\
  /          \  70% Unit Tests (Thuần túy JUnit 5 + Mockito cho tầng Service & Utility)
 /------------\
```

---

## 2. Quy chuẩn đặt tên Test Case (Naming Conventions)

Mỗi phương thức kiểm thử phải giải thích rõ ràng **Bối cảnh (Given)**, **Hành động (When)**, và **Kết quả mong đợi (Then)**:

### Cú pháp 1: BDD Style với `@DisplayName` (Khuyên dùng)
```java
@Test
@DisplayName("Should return CourseResponse when ID exists")
void shouldReturnCourseResponse_whenIdExists() { ... }

@Test
@DisplayName("Should throw ResourceNotFoundException when Course ID does not exist")
void shouldThrowNotFound_whenIdDoesNotExist() { ... }
```

### Cú pháp 2: Pattern `methodName_condition_expectedResult`
```java
@Test
void getById_validId_returnsResponseDTO() { ... }

@Test
void create_duplicateEmail_throwsConflictException() { ... }
```

---

## 3. Unit Test Tầng Service với Mockito thuần túy (Nhanh & Độc lập)

Tầng Service là nơi chứa logic nghiệp vụ quan trọng nhất. Cần kiểm thử 100% bằng Mockito thuần túy mà không khởi động Spring Context để đạt tốc độ thực thi miligiây:

```java
package com.company.project.service;

import com.company.project.common.exception.ResourceNotFoundException;
import com.company.project.dto.response.CourseResponse;
import com.company.project.entity.Course;
import com.company.project.repository.CourseRepository;
import com.company.project.service.impl.CourseServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class CourseServiceImplTest {

    @Mock
    private CourseRepository courseRepository;

    @InjectMocks
    private CourseServiceImpl courseService;

    @Test
    @DisplayName("Should return course details when valid ID is provided")
    void getById_existingId_success() {
        // Given (Chuẩn bị dữ liệu mẫu)
        Long courseId = 1L;
        Course mockCourse = new Course();
        mockCourse.setId(courseId);
        mockCourse.setTitle("Spring Boot Mastery");
        given(courseRepository.findById(courseId)).willReturn(Optional.of(mockCourse));

        // When (Thực thi phương thức)
        CourseResponse result = courseService.getById(courseId);

        // Then (Xác thực kết quả)
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(courseId);
        assertThat(result.getTitle()).isEqualTo("Spring Boot Mastery");
        verify(courseRepository).findById(courseId); // Đảm bảo repository được gọi đúng 1 lần
    }

    @Test
    @DisplayName("Should throw ResourceNotFoundException when course ID does not exist")
    void getById_nonExistingId_throwsException() {
        // Given
        Long courseId = 999L;
        given(courseRepository.findById(courseId)).willReturn(Optional.empty());

        // When & Then
        assertThatThrownBy(() -> courseService.getById(courseId))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("999");
    }
}
```

---

## 4. Slice Test Tầng Controller với `@WebMvcTest`

Chỉ khởi động MVC slice (không nạp DB, không nạp Service thật). Mock tầng Service bằng `@MockBean`:

```java
package com.company.project.controller;

import com.company.project.dto.response.CourseResponse;
import com.company.project.service.CourseService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(CourseController.class)
@AutoConfigureMockMvc(addFilters = false) // Tắt security filter nếu chỉ test controller routing
class CourseControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private CourseService courseService;

    @Test
    @DisplayName("GET /api/v1/courses/{id} should return 200 OK with course data")
    void getCourseById_success() throws Exception {
        CourseResponse response = CourseResponse.builder()
                .id(1L)
                .title("Java Spring Boot")
                .build();
        given(courseService.getById(1L)).willReturn(response);

        mockMvc.perform(get("/api/v1/courses/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.id").value(1))
                .andExpect(jsonPath("$.data.title").value("Java Spring Boot"));
    }
}
```

---

## 5. Quy chuẩn On-Demand Testing (Kiểm thử theo yêu cầu)

Để tối ưu hóa tài nguyên máy tính và chu kỳ phát triển của Coding Agent:
1. **Không tự động viết lại test:** Sau mỗi lần sửa logic hoặc refactor, Agent chỉ kiểm tra tính hợp lệ bằng lệnh biên dịch `mvnw test-compile`.
2. **Chỉ viết và chạy test khi có yêu cầu trực tiếp:** Khi người dùng yêu cầu "viết test cho tính năng X" hoặc "chạy test kiểm tra toàn bộ hệ thống", Agent mới thực hiện viết test và chạy `mvnw test`.
