package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.service.impl.CourseServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CourseServiceImplTest {

    @Mock
    private ICourseDao courseDao;

    @InjectMocks
    private CourseServiceImpl courseService;

    @Test
    @DisplayName("Create course saves entity via ICourseDao")
    void testCreateCourse() {
        CourseRequestDTO req = CourseRequestDTO.builder()
                .title("Spring Boot 3")
                .description("Generic DAO architecture")
                .duration(40)
                .price(399.0)
                .build();

        when(courseDao.save(any(Course.class))).thenAnswer(inv -> {
            Course c = inv.getArgument(0);
            c.setId(1L);
            return c;
        });

        Course saved = courseService.create(req);
        assertNotNull(saved);
        assertEquals(1L, saved.getId());
        assertEquals("Spring Boot 3", saved.getTitle());
        verify(courseDao, times(1)).save(any(Course.class));
    }

    @Test
    @DisplayName("Update course throws ResourceNotFoundException when missing")
    void testUpdateCourseNotFound() {
        when(courseDao.getById(99L)).thenReturn(null);
        CourseRequestDTO req = CourseRequestDTO.builder().title("Updated").duration(10).price(100.0).build();
        assertThrows(ResourceNotFoundException.class, () -> courseService.update(req, 99L));
    }

    @Test
    @DisplayName("Get course by ID returns mapped CourseResponseDTO")
    void testGetCourseById() {
        Course course = Course.builder()
                .id(5L)
                .title("Java 21")
                .description("Modern Java")
                .duration(30)
                .price(250.0)
                .build();
        when(courseDao.getById(5L)).thenReturn(course);

        CourseResponseDTO dto = courseService.getById(5L);
        assertEquals(5L, dto.getId());
        assertEquals("Java 21", dto.getTitle());
        assertEquals(250.0, dto.getPrice());
    }

    @Test
    @DisplayName("Filter courses by price range maps all matched entities")
    void testFilterByPrice() {
        when(courseDao.findByPriceRange(100.0, 500.0)).thenReturn(List.of(
                Course.builder().id(1L).title("Course A").price(200.0).duration(20).build()
        ));

        List<CourseResponseDTO> results = courseService.filterByPrice(100.0, 500.0);
        assertEquals(1, results.size());
        assertEquals("Course A", results.get(0).getTitle());
    }

    @Test
    @DisplayName("Delete course calls courseDao.delete when entity exists")
    void testDeleteCourse() {
        Course course = Course.builder().id(2L).title("To Delete").build();
        when(courseDao.getById(2L)).thenReturn(course);

        courseService.delete(2L);
        verify(courseDao, times(1)).delete(2L);
    }
}
