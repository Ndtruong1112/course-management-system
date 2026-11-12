package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Request DTO for data encryption")
public class EncryptRequestDTO {

    @NotBlank(message = "Data to encrypt cannot be blank")
    @ApiModelProperty(value = "Plaintext string data to encrypt", required = true, example = "SensitiveStudentData123")
    private String data;
}
