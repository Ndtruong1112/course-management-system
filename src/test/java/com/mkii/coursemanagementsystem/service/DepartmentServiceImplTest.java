package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.service.impl.DepartmentServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DepartmentServiceImplTest {

    @Mock
    private IDepartmentDao departmentDao;

    @InjectMocks
    private DepartmentServiceImpl departmentService;

    @Test
    @DisplayName("Create department normalizes code to uppercase and trims name")
    void testCreateDepartmentSuccess() {
        DepartmentRequestDTO req = DepartmentRequestDTO.builder()
                .departmentCode(" cntt ")
                .departmentName(" Cong nghe thong tin ")
                .description("Khoa CNTT")
                .build();

        when(departmentDao.findByDepartmentCode("CNTT")).thenReturn(Optional.empty());
        when(departmentDao.save(any(Department.class))).thenAnswer(inv -> {
            Department d = inv.getArgument(0);
            d.setDepartmentId(1L);
            return d;
        });

        DepartmentResponseDTO res = departmentService.createDepartment(req);
        assertEquals(1L, res.getDepartmentId());
        assertEquals("CNTT", res.getDepartmentCode());
        assertEquals("Cong nghe thong tin", res.getDepartmentName());
    }

    @Test
    @DisplayName("Create department throws BadRequestException when code already exists")
    void testCreateDepartmentDuplicateCode() {
        when(departmentDao.findByDepartmentCode("CNTT"))
                .thenReturn(Optional.of(Department.builder().departmentId(1L).departmentCode("CNTT").build()));

        DepartmentRequestDTO req = DepartmentRequestDTO.builder()
                .departmentCode("cntt")
                .departmentName("IT")
                .build();

        assertThrows(BadRequestException.class, () -> departmentService.createDepartment(req));
        verify(departmentDao, never()).save(any());
    }

    @Test
    @DisplayName("Get department by ID throws ResourceNotFoundException when missing")
    void testGetDepartmentNotFound() {
        when(departmentDao.getById(99L)).thenReturn(null);
        assertThrows(ResourceNotFoundException.class, () -> departmentService.getDepartmentById(99L));
    }
}
