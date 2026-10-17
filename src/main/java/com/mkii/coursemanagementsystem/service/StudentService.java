package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.domain.Page;

import java.util.List;

public interface StudentService {

    Student create(StudentRequestDTO requestDTO);

    Student update(StudentRequestDTO requestDTO, Long id);

    void delete(Long id);

    StudentResponseDTO getById(Long id);

    List<StudentResponseDTO> getAll();

    List<StudentResponseDTO> searchByKeyword(String keyword);

    StudentResponseDTO getByEmail(String email);

    StudentResponseDTO getByField(String field, Object value);

    /** Find multiple students matching a specific field value (returns list). */
    List<StudentResponseDTO> findByFieldList(String field, Object value);

    /** Find students matching a field with pagination and sorting. */
    Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple students at once. */
    List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs);

    List<StudentResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all students sorted by a field ("fullName", "email", …) and direction ("asc"/"desc"). */
    List<StudentResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of students, sorted. */
    Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}
