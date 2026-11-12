package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Enrollment;

import java.util.List;
import java.util.Map;

public interface IEnrollmentDao extends IPaginationSortingDao<Long, Enrollment> {

    Enrollment save(Enrollment enrollment);

    Enrollment update(Enrollment enrollment);

    void delete(Long id);

    Enrollment getById(Long id);

    List<Enrollment> getAll();

    boolean existsByStudentAndCourse(Long studentId, Long courseId);

    List<Enrollment> findByStudentId(Long studentId);

    List<Enrollment> findByCourseId(Long courseId);

    List<Enrollment> searchByKeyword(String keyword);

    Map<String, Long> countGroupByStatus();

    Double sumEnrolledCourseRevenue();

    Integer getCount();
}
