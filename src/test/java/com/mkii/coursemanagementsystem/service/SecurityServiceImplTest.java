package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.service.impl.SecurityServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class SecurityServiceImplTest {

    private SecurityService securityService;

    @BeforeEach
    void setUp() {
        securityService = new SecurityServiceImpl();
    }

    @Test
    @DisplayName("Encrypt and decrypt round-trip succeeds with valid payload")
    void testEncryptDecryptSuccess() {
        String originalData = "SuperSecretStudentCredential2026";
        EncryptRequestDTO encryptRequest = EncryptRequestDTO.builder().data(originalData).build();

        EncryptResponseDTO encryptResponse = securityService.encrypt(encryptRequest);
        assertNotNull(encryptResponse);
        assertNotNull(encryptResponse.getEncryptedData());
        assertEquals("AES/CBC/PKCS5Padding", encryptResponse.getAlgorithm());
        assertNotEquals(originalData, encryptResponse.getEncryptedData());

        DecryptRequestDTO decryptRequest = DecryptRequestDTO.builder()
                .encryptedData(encryptResponse.getEncryptedData())
                .build();
        DecryptResponseDTO decryptResponse = securityService.decrypt(decryptRequest);
        assertNotNull(decryptResponse);
        assertEquals(originalData, decryptResponse.getDecryptedData());
    }

    @Test
    @DisplayName("Encrypt throws BadRequestException when request or data is null")
    void testEncryptValidation() {
        assertThrows(BadRequestException.class, () -> securityService.encrypt(null));
        assertThrows(BadRequestException.class, () -> securityService.encrypt(new EncryptRequestDTO(null)));
    }

    @Test
    @DisplayName("Decrypt throws BadRequestException when request or encryptedData is null or invalid")
    void testDecryptValidation() {
        assertThrows(BadRequestException.class, () -> securityService.decrypt(null));
        assertThrows(BadRequestException.class, () -> securityService.decrypt(new DecryptRequestDTO(null)));
        assertThrows(BadRequestException.class, () -> securityService.decrypt(new DecryptRequestDTO("not-valid-base64")));
    }
}
