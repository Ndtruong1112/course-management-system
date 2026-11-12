package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DashboardStatsDTO {

    private Integer totalCourses;
    private Integer totalStudents;
    private Integer totalDepartments;
    private Integer totalEnrollments;
    private Integer activeDocuments;
    private Double totalEnrollmentRevenue;
    private Map<String, Long> enrollmentsByStatus;
}
