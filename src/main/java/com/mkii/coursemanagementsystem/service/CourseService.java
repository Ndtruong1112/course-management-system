package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;

import java.util.List;

public interface CourseService {

    Course create(CourseRequestDTO requestDTO);

    Course update(CourseRequestDTO requestDTO, Long id);

    void delete(Long id);

    CourseResponseDTO getById(Long id);

    List<CourseResponseDTO> getAll();

    List<CourseResponseDTO> searchByTitle(String keyword);

    List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice);

    CourseResponseDTO getByTitle(String title);

    CourseResponseDTO getByField(String field, Object value);

    /** Find multiple courses matching a specific field value (returns list). */
    List<CourseResponseDTO> findByFieldList(String field, Object value);

    /** Find courses matching a field with pagination and sorting. */
    Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction);

    /** Bulk insert / create multiple courses at once. */
    List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs);

    List<CourseResponseDTO> searchBySpecification(String search);

    // ──────────── Sorting / Pagination ────────────

    /** Get all courses sorted by a field ("title", "price", …) and direction ("asc"/"desc"). */
    List<CourseResponseDTO> getAllSorted(String sortBy, String direction);

    /** Get a page of courses, sorted. */
    Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction);

    /** Specification search + sort (no page metadata). */
    List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Specification search + pagination + sort. */
    Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    Integer getCount();
}