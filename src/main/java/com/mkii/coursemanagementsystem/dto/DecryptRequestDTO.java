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
@ApiModel(description = "Request DTO for data decryption")
public class DecryptRequestDTO {

    @NotBlank(message = "Encrypted data to decrypt cannot be blank")
    @ApiModelProperty(value = "Base64 encoded encrypted ciphertext with prepended IV", required = true)
    private String encryptedData;
}
