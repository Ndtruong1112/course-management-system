package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.dto.DashboardStatsDTO;
import com.mkii.coursemanagementsystem.rest.DashboardRest;
import com.mkii.coursemanagementsystem.service.DashboardService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class DashboardRestImpl implements DashboardRest {

    private final DashboardService dashboardService;

    public DashboardRestImpl(DashboardService dashboardService) {
        this.dashboardService = dashboardService;
    }

    @Override
    public ResponseEntity<DashboardStatsDTO> getStats() {
        return ResponseEntity.ok(dashboardService.getStats());
    }

    @Override
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP", "service", "course-management-system"));
    }
}
