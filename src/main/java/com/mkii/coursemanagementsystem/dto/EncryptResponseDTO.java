package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Response DTO for data encryption")
public class EncryptResponseDTO {

    @ApiModelProperty(value = "Base64 encoded encrypted ciphertext with prepended IV")
    private String encryptedData;

    @ApiModelProperty(value = "Encryption algorithm used", example = "AES/CBC/PKCS5Padding")
    private String algorithm;
}
