package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.dao.ICourseDao;
import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.dto.DashboardStatsDTO;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.service.impl.DashboardServiceImpl;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DashboardServiceImplTest {

    @Mock
    private ICourseDao courseDao;

    @Mock
    private IStudentDao studentDao;

    @Mock
    private IDepartmentDao departmentDao;

    @Mock
    private IEnrollmentDao enrollmentDao;

    @Mock
    private IDocumentDao documentDao;

    @InjectMocks
    private DashboardServiceImpl dashboardService;

    @Test
    @DisplayName("Dashboard aggregates counts and enrollment revenue accurately")
    void testGetStats() {
        when(courseDao.getCount()).thenReturn(3);
        when(studentDao.getCount()).thenReturn(10);
        when(departmentDao.getCount()).thenReturn(3);
        when(enrollmentDao.getCount()).thenReturn(6);
        when(documentDao.getAllActive()).thenReturn(List.of(new Document(), new Document()));
        when(enrollmentDao.sumEnrolledCourseRevenue()).thenReturn(1548.0);
        when(enrollmentDao.countGroupByStatus()).thenReturn(Map.of("ENROLLED", 4L, "COMPLETED", 2L));

        DashboardStatsDTO stats = dashboardService.getStats();
        assertEquals(3, stats.getTotalCourses());
        assertEquals(10, stats.getTotalStudents());
        assertEquals(3, stats.getTotalDepartments());
        assertEquals(6, stats.getTotalEnrollments());
        assertEquals(2, stats.getActiveDocuments());
        assertEquals(1548.0, stats.getTotalEnrollmentRevenue());
        assertEquals(4L, stats.getEnrollmentsByStatus().get("ENROLLED"));
    }
}
