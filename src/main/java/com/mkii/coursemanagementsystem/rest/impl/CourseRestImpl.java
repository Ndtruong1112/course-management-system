package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.rest.CourseRest;
import com.mkii.coursemanagementsystem.service.CourseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(ApiConstants.BASE_COURSE_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class CourseRestImpl implements CourseRest {

    private static final Logger logger = LoggerFactory.getLogger(CourseRestImpl.class);

    @Autowired
    private CourseService courseService;

    @Override
    public ResponseEntity<Course> createCourse(@jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Creating new Course: {}", requestDTO.getTitle());
            Course course = courseService.create(requestDTO);
            return new ResponseEntity<>(course, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Course> updateCourse(Long id, @jakarta.validation.Valid CourseRequestDTO requestDTO) {
        try {
            logger.info("Updating Course: {}", id);
            Course course = courseService.update(requestDTO, id);
            return ResponseEntity.ok(course);
        } catch (Exception e) {
            logger.error("Error updating Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteCourse(Long id) {
        try {
            logger.info("Deleting Course: {}", id);
            courseService.delete(id);
            return ResponseEntity.ok("Course deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Course: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseById(Long id) {
        try {
            logger.info("Getting Course by id: {}", id);
            CourseResponseDTO responseDTO = courseService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCourses() {
        try {
            logger.info("Getting all Courses");
            List<CourseResponseDTO> list = courseService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByTitle(String title, String queryTitle) {
        try {
            String searchTitle = title != null ? title : queryTitle;
            logger.info("Getting Course by title: {}", searchTitle);
            CourseResponseDTO responseDTO = courseService.getByTitle(searchTitle);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by title: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> createCoursesBatch(List<CourseRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
            List<CourseResponseDTO> result = courseService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<CourseResponseDTO> getCourseByField(String field, String value) {
        try {
            logger.info("Getting Course by field: {} = {}", field, value);
            CourseResponseDTO responseDTO = courseService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Course by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getCoursesByFieldList(String field, String value) {
        try {
            logger.info("Getting Course list by field: {} = {}", field, value);
            List<CourseResponseDTO> list = courseService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Course list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getCoursesByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Course page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCourses(String keyword) {
        try {
            logger.info("Searching Courses by keyword: {}", keyword);
            List<CourseResponseDTO> list = courseService.searchByTitle(keyword);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> filterCoursesByPrice(Double minPrice, Double maxPrice) {
        try {
            logger.info("Filtering Courses by price: {} - {}", minPrice, maxPrice);
            List<CourseResponseDTO> list = courseService.filterByPrice(minPrice, maxPrice);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error filtering Courses by price: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecification(String search) {
        try {
            logger.info("Searching Courses by Specification: {}", search);
            List<CourseResponseDTO> list = courseService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<CourseResponseDTO>> getAllCoursesSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
            List<CourseResponseDTO> list = courseService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> getAllCoursesPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Courses: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<CourseResponseDTO>> searchCoursesBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec sorted: {}, {} {}", search, sortBy, direction);
            List<CourseResponseDTO> list = courseService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<CourseResponseDTO>> searchCoursesBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Courses by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<CourseResponseDTO> result = courseService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Courses by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getCourseCount() {
        try {
            logger.info("Getting Course count");
            Integer count = courseService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Course count: ", e);
            throw e;
        }
    }
}
