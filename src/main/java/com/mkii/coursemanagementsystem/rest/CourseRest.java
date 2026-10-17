package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

public interface CourseRest {

    @PostMapping(value = {"", "/create"})
    ResponseEntity<Course> createCourse(@jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @PutMapping(value = {"/{id}", "/update/{id}"})
    ResponseEntity<Course> updateCourse(@PathVariable Long id, @jakarta.validation.Valid @RequestBody CourseRequestDTO requestDTO);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteCourse(@PathVariable Long id);

    @GetMapping("/{id}")
    ResponseEntity<CourseResponseDTO> getCourseById(@PathVariable Long id);

    @GetMapping(value = {"", "/list"})
    ResponseEntity<List<CourseResponseDTO>> getAllCourses();

    @GetMapping(value = {"/title/{title}", "/by-title"})
    ResponseEntity<CourseResponseDTO> getCourseByTitle(
            @PathVariable(required = false) String title,
            @RequestParam(required = false) String queryTitle);

    @PostMapping("/batch")
    ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(@RequestBody List<CourseRequestDTO> requestDTOs);

    @GetMapping("/by-field")
    ResponseEntity<CourseResponseDTO> getCourseByField(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-list")
    ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(
            @RequestParam String field,
            @RequestParam String value);

    @GetMapping("/by-field-paged")
    ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            @RequestParam String field,
            @RequestParam String value,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<CourseResponseDTO>> searchCourses(@RequestParam String keyword);

    @GetMapping("/filter")
    ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(
            @RequestParam Double minPrice,
            @RequestParam Double maxPrice);

    @GetMapping("/spec-search")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(@RequestParam String search);

    // ──────────── Sorting / Pagination endpoints ────────────

    /**
     * GET /api/courses/sorted?sortBy=title&direction=asc
     * Returns all courses sorted by one field.
     */
    @GetMapping("/sorted")
    ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/paged?page=0&size=10&sortBy=price&direction=desc
     * Returns a page of courses with metadata (totalElements, totalPages, …).
     */
    @GetMapping("/paged")
    ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-sorted?search=price>100&sortBy=price&direction=asc
     * Specification filter + sort, returns flat list.
     */
    @GetMapping("/spec-search-sorted")
    ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(
            @RequestParam String search,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    /**
     * GET /api/courses/spec-search-paged?search=price>100&page=0&size=5&sortBy=price&direction=asc
     * Specification filter + pagination + sort.
     */
    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "asc") String direction);

    @GetMapping("/count")
    ResponseEntity<Integer> getCourseCount();
}
