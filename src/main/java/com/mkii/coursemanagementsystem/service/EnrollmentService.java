package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.EnrollmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.EnrollmentResponseDTO;
import org.springframework.data.domain.Page;

import java.util.List;

public interface EnrollmentService {

    EnrollmentResponseDTO enroll(EnrollmentRequestDTO requestDTO);

    EnrollmentResponseDTO update(Long id, EnrollmentRequestDTO requestDTO);

    void delete(Long id);

    EnrollmentResponseDTO getById(Long id);

    List<EnrollmentResponseDTO> getAll();

    List<EnrollmentResponseDTO> getByStudentId(Long studentId);

    List<EnrollmentResponseDTO> getByCourseId(Long courseId);

    List<EnrollmentResponseDTO> search(String keyword);

    Page<EnrollmentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);
}
