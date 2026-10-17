package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface StudentRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Student> createStudent(@jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Student> updateStudent(@PathVariable Long id, @jakarta.validation.Valid @RequestBody StudentRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteStudent(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<StudentResponseDTO> getStudentById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<StudentResponseDTO>> getAllStudents();

    @GetMapping(value = {"/email/{email}", "/by-email"})
    ResponseEntity<StudentResponseDTO> getStudentByEmail(
            @PathVariable(required = false) String email,
            @RequestParam(required = false) String queryEmail);

    @PostMapping("/batch")
    ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(@RequestBody List<StudentRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<StudentResponseDTO> getStudentByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<StudentResponseDTO>> searchStudents(@RequestParam String keyword);

    @GetMapping("/spec-search")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/students/sorted?sortBy=fullName&direction=asc
     * Returns all students sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/paged?page=0&size=10&sortBy=fullName&direction=asc
     * Returns a page of students with metadata.
     */
    @GetMapping("/paged")
    ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-sorted?search=email:test@&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/students/spec-search-paged?search=email:test@&page=0&size=5&sortBy=fullName&direction=asc
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getStudentCount();
}
