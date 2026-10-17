package com.mkii.coursemanagementsystem.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CourseRequestDTO {

    @NotBlank(message = "Tiêu đề khóa học không được để trống")
    @Size(max = 255, message = "Tiêu đề khóa học không được vượt quá 255 ký tự")
    private String title;

    private String description;

    @NotNull(message = "Thời lượng khóa học không được để trống")
    @PositiveOrZero(message = "Thời lượng khóa học phải lớn hơn hoặc bằng 0")
    private Integer duration;

    @NotNull(message = "Học phí khóa học không được để trống")
    @PositiveOrZero(message = "Học phí khóa học phải lớn hơn hoặc bằng 0")
    private Double price;
}