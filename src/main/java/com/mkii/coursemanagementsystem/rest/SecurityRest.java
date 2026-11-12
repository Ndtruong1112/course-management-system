package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import io.swagger.annotations.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Api(tags = {"SecurityRest"})
@SwaggerDefinition(tags = {@Tag(name = "SecurityRest", description = "REST APIs for AES Encryption and Decryption")})
public interface SecurityRest {

    @PostMapping("/encrypt")
    @ApiOperation(value = "Encrypt plaintext payload with AES", tags = {"encrypt"}, authorizations = {
            @Authorization(value = "default", scopes = {
                    @AuthorizationScope(scope = "ROLE_ADMIN", description = "Admin role"),
                    @AuthorizationScope(scope = "ROLE_LECTURER", description = "Lecturer role")
            })
    })
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Success|OK", response = EncryptResponseDTO.class),
            @ApiResponse(code = 400, message = "Bad Request"),
            @ApiResponse(code = 403, message = "Access is denied")
    })
    @PreAuthorize("hasRole('ADMIN') or hasRole('TEACHER') or hasRole('LECTURER')")
    ResponseEntity<EncryptResponseDTO> encrypt(@Valid @RequestBody EncryptRequestDTO request);

    @PostMapping("/decrypt")
    @ApiOperation(value = "Decrypt ciphertext payload with AES", tags = {"decrypt"}, authorizations = {
            @Authorization(value = "default", scopes = {
                    @AuthorizationScope(scope = "ROLE_ADMIN", description = "Admin role"),
                    @AuthorizationScope(scope = "ROLE_TEACHER", description = "Teacher role"),
                    @AuthorizationScope(scope = "ROLE_LECTURER", description = "Lecturer role")
            })
    })
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Success|OK", response = DecryptResponseDTO.class),
            @ApiResponse(code = 400, message = "Bad Request"),
            @ApiResponse(code = 403, message = "Access is denied")
    })
    @PreAuthorize("hasRole('ADMIN') or hasRole('TEACHER') or hasRole('LECTURER')")
    ResponseEntity<DecryptResponseDTO> decrypt(@Valid @RequestBody DecryptRequestDTO request);
}
