package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.dto.EnrollmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.EnrollmentResponseDTO;
import com.mkii.coursemanagementsystem.rest.EnrollmentRest;
import com.mkii.coursemanagementsystem.service.EnrollmentService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class EnrollmentRestImpl implements EnrollmentRest {

    private final EnrollmentService enrollmentService;

    public EnrollmentRestImpl(EnrollmentService enrollmentService) {
        this.enrollmentService = enrollmentService;
    }

    @Override
    public ResponseEntity<EnrollmentResponseDTO> enroll(@Valid EnrollmentRequestDTO requestDTO) {
        return new ResponseEntity<>(enrollmentService.enroll(requestDTO), HttpStatus.CREATED);
    }

    @Override
    public ResponseEntity<EnrollmentResponseDTO> update(Long id, @Valid EnrollmentRequestDTO requestDTO) {
        return ResponseEntity.ok(enrollmentService.update(id, requestDTO));
    }

    @Override
    public ResponseEntity<Void> delete(Long id) {
        enrollmentService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @Override
    public ResponseEntity<EnrollmentResponseDTO> getById(Long id) {
        return ResponseEntity.ok(enrollmentService.getById(id));
    }

    @Override
    public ResponseEntity<List<EnrollmentResponseDTO>> getAll() {
        return ResponseEntity.ok(enrollmentService.getAll());
    }

    @Override
    public ResponseEntity<List<EnrollmentResponseDTO>> getByStudent(Long studentId) {
        return ResponseEntity.ok(enrollmentService.getByStudentId(studentId));
    }

    @Override
    public ResponseEntity<List<EnrollmentResponseDTO>> getByCourse(Long courseId) {
        return ResponseEntity.ok(enrollmentService.getByCourseId(courseId));
    }

    @Override
    public ResponseEntity<List<EnrollmentResponseDTO>> search(String keyword) {
        return ResponseEntity.ok(enrollmentService.search(keyword));
    }

    @Override
    public ResponseEntity<Page<EnrollmentResponseDTO>> getAllPaged(int page, int size, String sortBy, String direction) {
        return ResponseEntity.ok(enrollmentService.getAllPaged(page, size, sortBy, direction));
    }
}
