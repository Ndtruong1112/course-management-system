package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.EnrollmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.EnrollmentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.entity.Enrollment;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.impl.EnrollmentServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class EnrollmentServiceImplTest {

    @Mock
    private IEnrollmentDao enrollmentDao;

    @Mock
    private IStudentDao studentDao;

    @Mock
    private ICourseDao courseDao;

    @InjectMocks
    private EnrollmentServiceImpl enrollmentService;

    @Test
    @DisplayName("Enroll succeeds and auto-marks COMPLETED when progress is 100")
    void testEnrollSuccessAutoComplete() {
        Student student = Student.builder().id(1L).fullName("Nguyen Van A").email("a@school.edu.vn").build();
        Course course = Course.builder().id(2L).title("Spring Boot 3").price(499.0).build();
        EnrollmentRequestDTO req = EnrollmentRequestDTO.builder()
                .studentId(1L)
                .courseId(2L)
                .progressPercent(100)
                .notes("Fast track")
                .build();

        when(studentDao.getById(1L)).thenReturn(student);
        when(courseDao.getById(2L)).thenReturn(course);
        when(enrollmentDao.existsByStudentAndCourse(1L, 2L)).thenReturn(false);
        when(enrollmentDao.save(any(Enrollment.class))).thenAnswer(inv -> {
            Enrollment e = inv.getArgument(0);
            e.setId(50L);
            return e;
        });

        EnrollmentResponseDTO res = enrollmentService.enroll(req);
        assertEquals(50L, res.getId());
        assertEquals("COMPLETED", res.getStatus());
        assertEquals("Spring Boot 3", res.getCourseTitle());
        verify(enrollmentDao, times(1)).save(any(Enrollment.class));
    }

    @Test
    @DisplayName("Enroll throws BadRequestException on duplicate enrollment")
    void testEnrollDuplicateThrows() {
        Student student = Student.builder().id(1L).fullName("A").build();
        Course course = Course.builder().id(2L).title("C").build();
        when(studentDao.getById(1L)).thenReturn(student);
        when(courseDao.getById(2L)).thenReturn(course);
        when(enrollmentDao.existsByStudentAndCourse(1L, 2L)).thenReturn(true);

        EnrollmentRequestDTO req = EnrollmentRequestDTO.builder().studentId(1L).courseId(2L).build();
        assertThrows(BadRequestException.class, () -> enrollmentService.enroll(req));
        verify(enrollmentDao, never()).save(any());
    }

    @Test
    @DisplayName("Enroll throws ResourceNotFoundException when student missing")
    void testEnrollStudentMissing() {
        when(studentDao.getById(99L)).thenReturn(null);
        EnrollmentRequestDTO req = EnrollmentRequestDTO.builder().studentId(99L).courseId(2L).build();
        assertThrows(ResourceNotFoundException.class, () -> enrollmentService.enroll(req));
    }

    @Test
    @DisplayName("Update enrollment changes progress and status cleanly")
    void testUpdateProgress() {
        Student student = Student.builder().id(1L).fullName("A").email("a@x.com").build();
        Course course = Course.builder().id(2L).title("Java 21").price(300.0).build();
        Enrollment existing = Enrollment.builder()
                .id(10L)
                .student(student)
                .course(course)
                .status("ENROLLED")
                .progressPercent(20)
                .enrolledAt(LocalDateTime.now())
                .build();
        when(enrollmentDao.getById(10L)).thenReturn(existing);
        when(enrollmentDao.update(any(Enrollment.class))).thenAnswer(inv -> inv.getArgument(0));

        EnrollmentRequestDTO req = EnrollmentRequestDTO.builder()
                .studentId(1L)
                .courseId(2L)
                .progressPercent(80)
                .notes("Milestone 2")
                .build();

        EnrollmentResponseDTO updated = enrollmentService.update(10L, req);
        assertEquals(80, updated.getProgressPercent());
        assertEquals("Milestone 2", updated.getNotes());
    }

    @Test
    @DisplayName("Get enrollments by student delegates to DAO")
    void testGetByStudent() {
        Student student = Student.builder().id(1L).fullName("A").build();
        Course course = Course.builder().id(2L).title("C1").build();
        Enrollment e = Enrollment.builder().id(3L).student(student).course(course).status("ENROLLED").progressPercent(10).build();
        when(enrollmentDao.findByStudentId(1L)).thenReturn(List.of(e));

        List<EnrollmentResponseDTO> list = enrollmentService.getByStudentId(1L);
        assertEquals(1, list.size());
        assertEquals("C1", list.get(0).getCourseTitle());
    }
}
