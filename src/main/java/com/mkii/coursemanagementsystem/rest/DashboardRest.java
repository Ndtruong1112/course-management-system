package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.DashboardStatsDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.Map;

@RequestMapping(ApiConstants.BASE_DASHBOARD_URL)
public interface DashboardRest {

    @GetMapping("/stats")
    ResponseEntity<DashboardStatsDTO> getStats();

    @GetMapping("/health")
    ResponseEntity<Map<String, String>> health();
}
