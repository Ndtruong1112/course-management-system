package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.rest.SecurityRest;
import com.mkii.coursemanagementsystem.service.SecurityService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(ApiConstants.BASE_SECURITY_URL)
public class SecurityRestImpl implements SecurityRest {

    private static final Logger logger = LoggerFactory.getLogger(SecurityRestImpl.class);

    private final SecurityService securityService;

    public SecurityRestImpl(SecurityService securityService) {
        this.securityService = securityService;
    }

    @Override
    public ResponseEntity<EncryptResponseDTO> encrypt(@Valid EncryptRequestDTO request) {
        try {
            logger.info("REST: Encrypting request payload");
            EncryptResponseDTO response = securityService.encrypt(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("REST: Error during encrypt: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<DecryptResponseDTO> decrypt(@Valid DecryptRequestDTO request) {
        try {
            logger.info("REST: Decrypting request payload");
            DecryptResponseDTO response = securityService.decrypt(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            logger.error("REST: Error during decrypt: ", e);
            throw e;
        }
    }
}
