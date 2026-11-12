package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EnrollmentRequestDTO {

    @NotNull(message = "studentId không được để trống")
    private Long studentId;

    @NotNull(message = "courseId không được để trống")
    private Long courseId;

    @Pattern(regexp = "ENROLLED|COMPLETED|DROPPED", message = "Trạng thái chỉ nhận ENROLLED, COMPLETED hoặc DROPPED")
    private String status;

    @Min(value = 0, message = "Tiến độ tối thiểu là 0%")
    @Max(value = 100, message = "Tiến độ tối đa là 100%")
    private Integer progressPercent;

    @Size(max = 500, message = "Ghi chú không vượt quá 500 ký tự")
    private String notes;
}
