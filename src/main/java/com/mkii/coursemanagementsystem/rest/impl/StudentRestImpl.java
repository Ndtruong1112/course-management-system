package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.rest.StudentRest;
import com.mkii.coursemanagementsystem.service.StudentService;
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
@RequestMapping(ApiConstants.BASE_STUDENT_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class StudentRestImpl implements StudentRest {

    private static final Logger logger = LoggerFactory.getLogger(StudentRestImpl.class);

    @Autowired
    private StudentService studentService;

    @Override
    public ResponseEntity<Student> createStudent(@jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Creating new Student: {}", requestDTO.getFullName());
            Student student = studentService.create(requestDTO);
            return new ResponseEntity<>(student, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error creating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Student> updateStudent(Long id, @jakarta.validation.Valid StudentRequestDTO requestDTO) {
        try {
            logger.info("Updating Student: {}", id);
            Student student = studentService.update(requestDTO, id);
            return ResponseEntity.ok(student);
        } catch (Exception e) {
            logger.error("Error updating Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteStudent(Long id) {
        try {
            logger.info("Deleting Student: {}", id);
            studentService.delete(id);
            return ResponseEntity.ok("Student deleted successfully");
        } catch (Exception e) {
            logger.error("Error deleting Student: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentById(Long id) {
        try {
            logger.info("Getting Student by id: {}", id);
            StudentResponseDTO responseDTO = studentService.getById(id);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudents() {
        try {
            logger.info("Getting all Students");
            List<StudentResponseDTO> list = studentService.getAll();
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting all Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByEmail(String email, String queryEmail) {
        try {
            String searchEmail = email != null ? email : queryEmail;
            logger.info("Getting Student by email: {}", searchEmail);
            StudentResponseDTO responseDTO = studentService.getByEmail(searchEmail);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by email: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> createStudentsBatch(List<StudentRequestDTO> requestDTOs) {
        try {
            logger.info("Batch creating {} Students", requestDTOs != null ? requestDTOs.size() : 0);
            List<StudentResponseDTO> result = studentService.createBatch(requestDTOs);
            return new ResponseEntity<>(result, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error batch creating Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<StudentResponseDTO> getStudentByField(String field, String value) {
        try {
            logger.info("Getting Student by field: {} = {}", field, value);
            StudentResponseDTO responseDTO = studentService.getByField(field, value);
            return ResponseEntity.ok(responseDTO);
        } catch (Exception e) {
            logger.error("Error getting Student by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getStudentsByFieldList(String field, String value) {
        try {
            logger.info("Getting Student list by field: {} = {}", field, value);
            List<StudentResponseDTO> list = studentService.findByFieldList(field, value);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting Student list by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getStudentsByFieldPaged(
            String field, String value, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.findByFieldPaged(field, value, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting Student page by field: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudents(String keyword) {
        try {
            logger.info("Searching Students by keyword: {}", keyword);
            List<StudentResponseDTO> list = studentService.searchByKeyword(keyword);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecification(String search) {
        try {
            logger.info("Searching Students by Specification: {}", search);
            List<StudentResponseDTO> list = studentService.searchBySpecification(search);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by Specification: ", e);
            throw e;
        }
    }

    // ──────────── Sorting / Pagination ────────────

    @Override
    public ResponseEntity<List<StudentResponseDTO>> getAllStudentsSorted(String sortBy, String direction) {
        try {
            logger.info("Getting all Students sorted by {} {}", sortBy, direction);
            List<StudentResponseDTO> list = studentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error getting sorted Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> getAllStudentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error getting paged Students: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<StudentResponseDTO>> searchStudentsBySpecificationSorted(String search, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec sorted: {}, {} {}", search, sortBy, direction);
            List<StudentResponseDTO> list = studentService.searchBySpecificationSorted(search, sortBy, direction);
            return ResponseEntity.ok(list);
        } catch (Exception e) {
            logger.error("Error searching Students by spec sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<StudentResponseDTO>> searchStudentsBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("Searching Students by spec paged: {}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<StudentResponseDTO> result = studentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("Error searching Students by spec paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getStudentCount() {
        try {
            logger.info("Getting Student count");
            Integer count = studentService.getCount();
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("Error getting Student count: ", e);
            throw e;
        }
    }
}
