package com.mkii.coursemanagementsystem.dto;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ApiModel(description = "Response DTO for data decryption")
public class DecryptResponseDTO {

    @ApiModelProperty(value = "Decrypted original plaintext string")
    private String decryptedData;
}
