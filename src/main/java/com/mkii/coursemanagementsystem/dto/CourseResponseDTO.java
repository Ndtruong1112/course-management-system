package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseResponseDTO {
    private Long id;
    private String title;
    private String description;
    private Integer duration;
    private Double price;
}