package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dto.DepartmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.DepartmentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.service.DepartmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class DepartmentServiceImpl implements DepartmentService {

    private static final Logger logger = LoggerFactory.getLogger(DepartmentServiceImpl.class);

    private final IDepartmentDao departmentDao;

    public DepartmentServiceImpl(IDepartmentDao departmentDao) {
        this.departmentDao = departmentDao;
    }

    @Override
    public DepartmentResponseDTO createDepartment(DepartmentRequestDTO dto) {
        if (dto.getDepartmentCode() == null || dto.getDepartmentCode().trim().isEmpty()) {
            throw new BadRequestException("Mã khoa không được để trống.");
        }
        String normalizedCode = dto.getDepartmentCode().trim().toUpperCase();
        logger.info("Creating Department with code: {}", normalizedCode);
        if (departmentDao.findByDepartmentCode(normalizedCode).isPresent()) {
            throw new BadRequestException("Mã khoa đã tồn tại: " + normalizedCode);
        }

        Department department = Department.builder()
                .departmentCode(normalizedCode)
                .departmentName(dto.getDepartmentName() != null ? dto.getDepartmentName().trim() : "")
                .description(dto.getDescription())
                .build();

        Department saved = departmentDao.save(department);
        return toDTO(saved);
    }

    @Override
    public DepartmentResponseDTO updateDepartment(Long id, DepartmentRequestDTO dto) {
        logger.info("Updating Department with ID: {}", id);
        Department existing = departmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }

        if (dto.getDepartmentCode() != null && !dto.getDepartmentCode().trim().isEmpty()) {
            String normalizedCode = dto.getDepartmentCode().trim().toUpperCase();
            departmentDao.findByDepartmentCode(normalizedCode).ifPresent(d -> {
                if (!d.getDepartmentId().equals(id)) {
                    throw new BadRequestException("Mã khoa đã tồn tại: " + normalizedCode);
                }
            });
            existing.setDepartmentCode(normalizedCode);
        }

        if (dto.getDepartmentName() != null) {
            existing.setDepartmentName(dto.getDepartmentName().trim());
        }
        existing.setDescription(dto.getDescription());

        Department updated = departmentDao.update(existing);
        return toDTO(updated);
    }

    @Override
    public void deleteDepartment(Long id) {
        logger.info("Deleting Department with ID: {}", id);
        Department existing = departmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }
        departmentDao.delete(id);
    }

    @Override
    @Transactional(readOnly = true)
    public DepartmentResponseDTO getDepartmentById(Long id) {
        Department department = departmentDao.getById(id);
        if (department == null) {
            throw new ResourceNotFoundException("Department not found with id: " + id);
        }
        return toDTO(department);
    }

    @Override
    @Transactional(readOnly = true)
    public DepartmentResponseDTO getDepartmentByCode(String code) {
        return departmentDao.findByDepartmentCode(code)
                .map(this::toDTO)
                .orElseThrow(() -> new ResourceNotFoundException("Department not found with code: " + code));
    }

    @Override
    @Transactional(readOnly = true)
    public List<DepartmentResponseDTO> getAllDepartments() {
        return departmentDao.getAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<DepartmentResponseDTO> searchDepartments(String keyword) {
        return departmentDao.searchByName(keyword).stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private DepartmentResponseDTO toDTO(Department d) {
        return DepartmentResponseDTO.builder()
                .departmentId(d.getDepartmentId())
                .departmentCode(d.getDepartmentCode())
                .departmentName(d.getDepartmentName())
                .description(d.getDescription())
                .createdAt(d.getCreatedAt())
                .updatedAt(d.getUpdatedAt())
                .build();
    }
}
