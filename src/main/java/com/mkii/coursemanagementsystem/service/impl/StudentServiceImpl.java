package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.StudentRequestDTO;
import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.StudentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class StudentServiceImpl implements StudentService {

    private static final Logger logger = LoggerFactory.getLogger(StudentServiceImpl.class);

    // Call ONLY IStudentDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private IStudentDao studentDao;

    @Override
    public Student create(StudentRequestDTO requestDTO) {
        logger.info("Creating Student: {}", requestDTO.getFullName());
        if (requestDTO.getEmail() != null) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        Student student = new Student();
        mapRequestToEntity(requestDTO, student);
        return studentDao.save(student);
    }

    @Override
    public Student update(StudentRequestDTO requestDTO, Long id) {
        logger.info("Updating Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        if (requestDTO.getEmail() != null && !requestDTO.getEmail().equalsIgnoreCase(existing.getEmail())) {
            Student existingByEmail = studentDao.getByEmail(requestDTO.getEmail());
            if (existingByEmail != null && !existingByEmail.getId().equals(id)) {
                throw new com.mkii.coursemanagementsystem.common.exception.BadRequestException("Email '" + requestDTO.getEmail() + "' đã được sử dụng bởi sinh viên khác.");
            }
        }
        mapRequestToEntity(requestDTO, existing);
        return studentDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        Student existing = studentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        studentDao.delete(id);
    }

    @Override
    public StudentResponseDTO getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        Student student = studentDao.getById(id);
        if (student == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, id));
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> getAll() {
        logger.info("Getting all Students");
        return studentDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return studentDao.searchByKeyword(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public StudentResponseDTO getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        Student student = studentDao.getByEmail(email);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với email: " + email);
        }
        return mapToDTO(student);
    }

    @Override
    public StudentResponseDTO getByField(String field, Object value) {
        logger.info("Getting Student by field: {} = {}", field, value);
        Student student = studentDao.getByField(field, value);
        if (student == null) {
            throw new ResourceNotFoundException("Không tìm thấy sinh viên với " + field + ": " + value);
        }
        return mapToDTO(student);
    }

    @Override
    public List<StudentResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Student list by field: {} = {}", field, value);
        return studentDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Student page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return studentDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> createBatch(List<StudentRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Students", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Student> entities = requestDTOs.stream().map(dto -> {
            Student student = new Student();
            mapRequestToEntity(dto, student);
            return student;
        }).collect(Collectors.toList());
        return studentDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to IStudentDao) ────────────

    @Override
    public List<StudentResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Students by Specification query: {}", search);
        return studentDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<StudentResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Students sorted by {} {}", sortBy, direction);
        return studentDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Students paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return studentDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<StudentResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Students by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return studentDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<StudentResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Students by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return studentDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return studentDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(StudentRequestDTO requestDTO, Student student) {
        if (requestDTO.getFullName() != null) {
            student.setFullName(requestDTO.getFullName());
        }
        if (requestDTO.getEmail() != null) {
            student.setEmail(requestDTO.getEmail());
        }
        if (requestDTO.getPhone() != null) {
            student.setPhone(requestDTO.getPhone());
        }
        if (requestDTO.getAddress() != null) {
            student.setAddress(requestDTO.getAddress());
        }
    }

    private StudentResponseDTO mapToDTO(Student student) {
        return new StudentResponseDTO(
                student.getId(),
                student.getFullName(),
                student.getEmail(),
                student.getPhone(),
                student.getAddress()
        );
    }
}
