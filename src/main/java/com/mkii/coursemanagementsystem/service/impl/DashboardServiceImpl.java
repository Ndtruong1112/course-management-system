package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.DashboardStatsDTO;
import com.mkii.coursemanagementsystem.service.DashboardService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.Map;

@Service
@Transactional(readOnly = true)
public class DashboardServiceImpl implements DashboardService {

    private final ICourseDao courseDao;
    private final IStudentDao studentDao;
    private final IDepartmentDao departmentDao;
    private final IEnrollmentDao enrollmentDao;
    private final IDocumentDao documentDao;

    public DashboardServiceImpl(ICourseDao courseDao,
                                IStudentDao studentDao,
                                IDepartmentDao departmentDao,
                                IEnrollmentDao enrollmentDao,
                                IDocumentDao documentDao) {
        this.courseDao = courseDao;
        this.studentDao = studentDao;
        this.departmentDao = departmentDao;
        this.enrollmentDao = enrollmentDao;
        this.documentDao = documentDao;
    }

    @Override
    public DashboardStatsDTO getStats() {
        Integer courses = courseDao.getCount();
        Integer students = studentDao.getCount();
        Integer departments = departmentDao.getCount();
        Integer enrollments = enrollmentDao.getCount();
        var activeDocs = documentDao.getAllActive();
        Integer documents = activeDocs != null ? activeDocs.size() : 0;
        Double revenue = enrollmentDao.sumEnrolledCourseRevenue();
        Map<String, Long> byStatus = enrollmentDao.countGroupByStatus();

        return DashboardStatsDTO.builder()
                .totalCourses(courses != null ? courses : 0)
                .totalStudents(students != null ? students : 0)
                .totalDepartments(departments != null ? departments : 0)
                .totalEnrollments(enrollments != null ? enrollments : 0)
                .activeDocuments(documents != null ? documents : 0)
                .totalEnrollmentRevenue(revenue != null ? revenue : 0.0)
                .enrollmentsByStatus(byStatus != null ? byStatus : Collections.emptyMap())
                .build();
    }
}
