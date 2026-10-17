package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dto.CourseRequestDTO;
import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.service.CourseService;
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
public class CourseServiceImpl implements CourseService {

    private static final Logger logger = LoggerFactory.getLogger(CourseServiceImpl.class);

    // Call ONLY ICourseDao (in dao package), never call Hibernate DAO directly
    @Autowired
    private ICourseDao courseDao;

    @Override
    public Course create(CourseRequestDTO requestDTO) {
        logger.info("Creating Course: {}", requestDTO.getTitle());
        Course course = new Course();
        mapRequestToEntity(requestDTO, course);
        return courseDao.save(course);
    }

    @Override
    public Course update(CourseRequestDTO requestDTO, Long id) {
        logger.info("Updating Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        mapRequestToEntity(requestDTO, existing);
        return courseDao.update(existing);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Course: {}", id);
        Course existing = courseDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        courseDao.delete(id);
    }

    @Override
    public CourseResponseDTO getById(Long id) {
        logger.info("Getting Course by id: {}", id);
        Course course = courseDao.getById(id);
        if (course == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, id));
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> getAll() {
        logger.info("Getting all Courses");
        return courseDao.getAll()
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> searchByTitle(String keyword) {
        logger.info("Searching Courses by title: {}", keyword);
        return courseDao.searchByTitle(keyword)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> filterByPrice(Double minPrice, Double maxPrice) {
        logger.info("Filtering Courses by price range: {} - {}", minPrice, maxPrice);
        return courseDao.findByPriceRange(minPrice, maxPrice)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public CourseResponseDTO getByTitle(String title) {
        logger.info("Getting Course by title: {}", title);
        Course course = courseDao.getByTitle(title);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với tiêu đề: " + title);
        }
        return mapToDTO(course);
    }

    @Override
    public CourseResponseDTO getByField(String field, Object value) {
        logger.info("Getting Course by field: {} = {}", field, value);
        Course course = courseDao.getByField(field, value);
        if (course == null) {
            throw new ResourceNotFoundException("Không tìm thấy khóa học với " + field + ": " + value);
        }
        return mapToDTO(course);
    }

    @Override
    public List<CourseResponseDTO> findByFieldList(String field, Object value) {
        logger.info("Finding Course list by field: {} = {}", field, value);
        return courseDao.findByField(field, value)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> findByFieldPaged(String field, Object value, int page, int size, String sortBy, String direction) {
        logger.info("Finding Course page by field: {} = {}, page={}, size={}, sort={} {}", field, value, page, size, sortBy, direction);
        return courseDao.findByFieldPaged(field, value, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> createBatch(List<CourseRequestDTO> requestDTOs) {
        logger.info("Creating batch of {} Courses", requestDTOs != null ? requestDTOs.size() : 0);
        if (requestDTOs == null || requestDTOs.isEmpty()) {
            return java.util.Collections.emptyList();
        }
        List<Course> entities = requestDTOs.stream().map(dto -> {
            Course course = new Course();
            mapRequestToEntity(dto, course);
            return course;
        }).collect(Collectors.toList());
        return courseDao.createAll(entities)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    // ──────────── Search, Sorting & Pagination (Delegated to ICourseDao) ────────────

    @Override
    public List<CourseResponseDTO> searchBySpecification(String search) {
        logger.info("Searching Courses by Specification query: {}", search);
        return courseDao.searchBySpecification(search)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<CourseResponseDTO> getAllSorted(String sortBy, String direction) {
        logger.info("Getting all Courses sorted by {} {}", sortBy, direction);
        return courseDao.findAllSorted(sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Getting all Courses paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return courseDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public List<CourseResponseDTO> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching Courses by spec sorted: search={}, sort={} {}", search, sortBy, direction);
        return courseDao.searchBySpecificationSorted(search, sortBy, direction)
                .stream()
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public Page<CourseResponseDTO> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching Courses by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return courseDao.searchBySpecificationPaged(search, page, size, sortBy, direction).map(this::mapToDTO);
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Course count");
        return courseDao.getCount();
    }

    // ──────────── Private helpers ────────────

    private void mapRequestToEntity(CourseRequestDTO requestDTO, Course course) {
        if (requestDTO.getTitle() != null) {
            course.setTitle(requestDTO.getTitle());
        }
        if (requestDTO.getDescription() != null) {
            course.setDescription(requestDTO.getDescription());
        }
        if (requestDTO.getDuration() != null) {
            course.setDuration(requestDTO.getDuration());
        }
        if (requestDTO.getPrice() != null) {
            course.setPrice(requestDTO.getPrice());
        }
    }

    private CourseResponseDTO mapToDTO(Course course) {
        return new CourseResponseDTO(
                course.getId(),
                course.getTitle(),
                course.getDescription(),
                course.getDuration(),
                course.getPrice()
        );
    }
}
