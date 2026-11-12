package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DepartmentRequestDTO {

    @NotBlank(message = "Department code is mandatory")
    @Size(max = 20, message = "Department code must not exceed 20 characters")
    private String departmentCode;

    @NotBlank(message = "Department name is mandatory")
    @Size(max = 100, message = "Department name must not exceed 100 characters")
    private String departmentName;

    @Size(max = 255, message = "Description must not exceed 255 characters")
    private String description;
}
