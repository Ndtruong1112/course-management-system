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
    private java.time.LocalDate dob;
    private DepartmentResponseDTO department;

    public StudentResponseDTO(Long id, String fullName, String email, String phone, String address) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
        this.address = address;
    }

    public StudentResponseDTO(Long id, String fullName, String email, String phone, String address, java.time.LocalDate dob) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.phone = phone;
        this.address = address;
        this.dob = dob;
    }
}
