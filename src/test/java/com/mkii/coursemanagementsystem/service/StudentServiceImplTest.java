package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.impl.StudentServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class StudentServiceImplTest {

    @Mock
    private IStudentDao studentDao;

    @Mock
    private IDepartmentDao departmentDao;

    @InjectMocks
    private StudentServiceImpl studentService;

    @Test
    @DisplayName("Create student assigns department and saves via IStudentDao")
    void testCreateStudentSuccess() {
        Department dept = Department.builder()
                .departmentId(1L)
                .departmentCode("CNTT")
                .departmentName("Cong nghe thong tin")
                .build();
        StudentRequestDTO req = StudentRequestDTO.builder()
                .fullName("Nguyen Van A")
                .email("vana@school.edu.vn")
                .phone("0912345678")
                .address("Hanoi")
                .dob(LocalDate.of(2003, 5, 10))
                .departmentId(1L)
                .build();

        when(studentDao.getByEmail("vana@school.edu.vn")).thenReturn(null);
        when(departmentDao.getById(1L)).thenReturn(dept);
        when(studentDao.save(any(Student.class))).thenAnswer(inv -> {
            Student s = inv.getArgument(0);
            s.setId(10L);
            return s;
        });

        Student created = studentService.create(req);
        assertEquals(10L, created.getId());
        assertEquals("CNTT", created.getDepartment().getDepartmentCode());
        verify(studentDao, times(1)).save(any(Student.class));
    }

    @Test
    @DisplayName("Create student throws BadRequestException on duplicate email")
    void testCreateStudentDuplicateEmail() {
        Student existing = Student.builder().id(1L).email("dup@school.edu.vn").build();
        when(studentDao.getByEmail("dup@school.edu.vn")).thenReturn(existing);

        StudentRequestDTO req = StudentRequestDTO.builder()
                .fullName("Dup User")
                .email("dup@school.edu.vn")
                .build();

        assertThrows(BadRequestException.class, () -> studentService.create(req));
        verify(studentDao, never()).save(any());
    }

    @Test
    @DisplayName("Get student by ID maps nested DepartmentResponseDTO")
    void testGetStudentById() {
        Department dept = Department.builder()
                .departmentId(2L)
                .departmentCode("KHMT")
                .departmentName("Khoa hoc may tinh")
                .build();
        Student student = Student.builder()
                .id(7L)
                .fullName("Tran Thi B")
                .email("thib@school.edu.vn")
                .department(dept)
                .build();
        when(studentDao.getById(7L)).thenReturn(student);

        StudentResponseDTO dto = studentService.getById(7L);
        assertEquals("Tran Thi B", dto.getFullName());
        assertNotNull(dto.getDepartment());
        assertEquals("KHMT", dto.getDepartment().getDepartmentCode());
    }

    @Test
    @DisplayName("Delete non-existent student throws ResourceNotFoundException")
    void testDeleteStudentNotFound() {
        when(studentDao.getById(404L)).thenReturn(null);
        assertThrows(ResourceNotFoundException.class, () -> studentService.delete(404L));
    }
}
