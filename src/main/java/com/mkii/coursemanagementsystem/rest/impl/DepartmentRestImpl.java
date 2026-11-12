package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import com.mkii.coursemanagementsystem.rest.DepartmentRest;
import com.mkii.coursemanagementsystem.service.DepartmentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class DepartmentRestImpl implements DepartmentRest {

    private final DepartmentService departmentService;

    public DepartmentRestImpl(DepartmentService departmentService) {
        this.departmentService = departmentService;
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> create(@Valid DepartmentRequestDTO dto) {
        DepartmentResponseDTO created = departmentService.createDepartment(dto);
        return new ResponseEntity<>(created, HttpStatus.CREATED);
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> update(Long id, @Valid DepartmentRequestDTO dto) {
        DepartmentResponseDTO updated = departmentService.updateDepartment(id, dto);
        return ResponseEntity.ok(updated);
    }

    @Override
    public ResponseEntity<Void> delete(Long id) {
        departmentService.deleteDepartment(id);
        return ResponseEntity.noContent().build();
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> getById(Long id) {
        return ResponseEntity.ok(departmentService.getDepartmentById(id));
    }

    @Override
    public ResponseEntity<DepartmentResponseDTO> getByCode(String code) {
        return ResponseEntity.ok(departmentService.getDepartmentByCode(code));
    }

    @Override
    public ResponseEntity<List<DepartmentResponseDTO>> getAll() {
        return ResponseEntity.ok(departmentService.getAllDepartments());
    }

    @Override
    public ResponseEntity<List<DepartmentResponseDTO>> search(String keyword) {
        return ResponseEntity.ok(departmentService.searchDepartments(keyword));
    }
}
