package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;

import java.util.List;

public interface DepartmentService {

    DepartmentResponseDTO createDepartment(DepartmentRequestDTO dto);

    DepartmentResponseDTO updateDepartment(Long id, DepartmentRequestDTO dto);

    void deleteDepartment(Long id);

    DepartmentResponseDTO getDepartmentById(Long id);

    DepartmentResponseDTO getDepartmentByCode(String code);

    List<DepartmentResponseDTO> getAllDepartments();

    List<DepartmentResponseDTO> searchDepartments(String keyword);
}
