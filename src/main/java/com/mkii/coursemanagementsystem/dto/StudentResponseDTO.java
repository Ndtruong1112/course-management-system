package com.mkii.coursemanagementsystem.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class StudentResponseDTO {
    private Long id;
    private String fullName;
    private String email;
    private String phone;
    private String address;
}
