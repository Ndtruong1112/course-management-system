package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.EnrollmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.EnrollmentResponseDTO;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping(ApiConstants.BASE_ENROLLMENT_URL)
public interface EnrollmentRest {

    @PostMapping
    ResponseEntity<EnrollmentResponseDTO> enroll(@RequestBody EnrollmentRequestDTO requestDTO);

    @PutMapping("/{id}")
    ResponseEntity<EnrollmentResponseDTO> update(@PathVariable("id") Long id, @RequestBody EnrollmentRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<Void> delete(@PathVariable("id") Long id);

    @GetMapping("/{id}")
    ResponseEntity<EnrollmentResponseDTO> getById(@PathVariable("id") Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<EnrollmentResponseDTO>> getAll();

    @GetMapping("/student/{studentId}")
    ResponseEntity<List<EnrollmentResponseDTO>> getByStudent(@PathVariable("studentId") Long studentId);

    @GetMapping("/course/{courseId}")
    ResponseEntity<List<EnrollmentResponseDTO>> getByCourse(@PathVariable("courseId") Long courseId);

    @GetMapping("/search")
    ResponseEntity<List<EnrollmentResponseDTO>> search(@RequestParam(value = "keyword", required = false, defaultValue = "") String keyword);

    @GetMapping("/paged")
    ResponseEntity<Page<EnrollmentResponseDTO>> getAllPaged(
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size,
            @RequestParam(value = "sortBy", defaultValue = "id") String sortBy,
            @RequestParam(value = "direction", defaultValue = "desc") String direction);
}
