package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.EnrollmentRequestDTO;
import com.mkii.coursemanagementsystem.dto.EnrollmentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.entity.Enrollment;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.service.EnrollmentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class EnrollmentServiceImpl implements EnrollmentService {

    private static final Logger logger = LoggerFactory.getLogger(EnrollmentServiceImpl.class);

    private final IEnrollmentDao enrollmentDao;
    private final IStudentDao studentDao;
    private final ICourseDao courseDao;

    public EnrollmentServiceImpl(IEnrollmentDao enrollmentDao,
                                 IStudentDao studentDao,
                                 ICourseDao courseDao) {
        this.enrollmentDao = enrollmentDao;
        this.studentDao = studentDao;
        this.courseDao = courseDao;
    }

    @Override
    public EnrollmentResponseDTO enroll(EnrollmentRequestDTO requestDTO) {
        Student student = studentDao.getById(requestDTO.getStudentId());
        if (student == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, requestDTO.getStudentId()));
        }
        Course course = courseDao.getById(requestDTO.getCourseId());
        if (course == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, requestDTO.getCourseId()));
        }
        if (enrollmentDao.existsByStudentAndCourse(student.getId(), course.getId())) {
            throw new BadRequestException(String.format(MessageConstants.ENROLLMENT_ALREADY_EXISTS, student.getId(), course.getId()));
        }

        int progress = requestDTO.getProgressPercent() != null ? requestDTO.getProgressPercent() : 0;
        String status = normalizeStatus(requestDTO.getStatus(), progress);

        Enrollment enrollment = Enrollment.builder()
                .student(student)
                .course(course)
                .status(status)
                .progressPercent(progress)
                .enrolledAt(LocalDateTime.now())
                .notes(requestDTO.getNotes())
                .build();

        Enrollment saved = enrollmentDao.save(enrollment);
        logger.info("Enrolled student {} in course {}", student.getId(), course.getId());
        return mapToDTO(saved);
    }

    @Override
    public EnrollmentResponseDTO update(Long id, EnrollmentRequestDTO requestDTO) {
        Enrollment existing = enrollmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.ENROLLMENT_NOT_FOUND, id));
        }
        if (requestDTO.getStudentId() != null && !requestDTO.getStudentId().equals(existing.getStudent().getId())) {
            Student student = studentDao.getById(requestDTO.getStudentId());
            if (student == null) {
                throw new ResourceNotFoundException(String.format(MessageConstants.STUDENT_NOT_FOUND, requestDTO.getStudentId()));
            }
            existing.setStudent(student);
        }
        if (requestDTO.getCourseId() != null && !requestDTO.getCourseId().equals(existing.getCourse().getId())) {
            Course course = courseDao.getById(requestDTO.getCourseId());
            if (course == null) {
                throw new ResourceNotFoundException(String.format(MessageConstants.COURSE_NOT_FOUND, requestDTO.getCourseId()));
            }
            existing.setCourse(course);
        }
        int progress = requestDTO.getProgressPercent() != null
                ? requestDTO.getProgressPercent()
                : (existing.getProgressPercent() != null ? existing.getProgressPercent() : 0);
        existing.setProgressPercent(progress);
        existing.setStatus(normalizeStatus(requestDTO.getStatus() != null ? requestDTO.getStatus() : existing.getStatus(), progress));
        if (requestDTO.getNotes() != null) {
            existing.setNotes(requestDTO.getNotes());
        }

        return mapToDTO(enrollmentDao.update(existing));
    }

    @Override
    public void delete(Long id) {
        Enrollment existing = enrollmentDao.getById(id);
        if (existing == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.ENROLLMENT_NOT_FOUND, id));
        }
        enrollmentDao.delete(id);
    }

    @Override
    @Transactional(readOnly = true)
    public EnrollmentResponseDTO getById(Long id) {
        Enrollment enrollment = enrollmentDao.getById(id);
        if (enrollment == null) {
            throw new ResourceNotFoundException(String.format(MessageConstants.ENROLLMENT_NOT_FOUND, id));
        }
        return mapToDTO(enrollment);
    }

    @Override
    @Transactional(readOnly = true)
    public List<EnrollmentResponseDTO> getAll() {
        return enrollmentDao.getAll().stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<EnrollmentResponseDTO> getByStudentId(Long studentId) {
        return enrollmentDao.findByStudentId(studentId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<EnrollmentResponseDTO> getByCourseId(Long courseId) {
        return enrollmentDao.findByCourseId(courseId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public List<EnrollmentResponseDTO> search(String keyword) {
        return enrollmentDao.searchByKeyword(keyword).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    @Transactional(readOnly = true)
    public Page<EnrollmentResponseDTO> getAllPaged(int page, int size, String sortBy, String direction) {
        return enrollmentDao.findAllPaged(page, size, sortBy, direction).map(this::mapToDTO);
    }

    private String normalizeStatus(String status, int progress) {
        if (status != null && !status.isBlank()) {
            return status.trim().toUpperCase();
        }
        return progress >= 100 ? "COMPLETED" : "ENROLLED";
    }

    private EnrollmentResponseDTO mapToDTO(Enrollment e) {
        return EnrollmentResponseDTO.builder()
                .id(e.getId())
                .studentId(e.getStudent() != null ? e.getStudent().getId() : null)
                .studentName(e.getStudent() != null ? e.getStudent().getFullName() : null)
                .studentEmail(e.getStudent() != null ? e.getStudent().getEmail() : null)
                .courseId(e.getCourse() != null ? e.getCourse().getId() : null)
                .courseTitle(e.getCourse() != null ? e.getCourse().getTitle() : null)
                .coursePrice(e.getCourse() != null ? e.getCourse().getPrice() : null)
                .status(e.getStatus())
                .progressPercent(e.getProgressPercent())
                .enrolledAt(e.getEnrolledAt())
                .notes(e.getNotes())
                .build();
    }
}
