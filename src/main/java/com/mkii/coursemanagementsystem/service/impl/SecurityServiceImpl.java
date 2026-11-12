package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.service.SecurityService;
import com.mkii.coursemanagementsystem.util.AESUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;

@Service
public class SecurityServiceImpl implements SecurityService {

    private static final Logger logger = LoggerFactory.getLogger(SecurityServiceImpl.class);
    private static final String DEFAULT_KEY = System.getenv("CMS_AES_KEY") != null
            ? System.getenv("CMS_AES_KEY") : "CourseManagementSystemSecretKey2026";
    private static final String DEFAULT_SALT = System.getenv("CMS_AES_SALT") != null
            ? System.getenv("CMS_AES_SALT") : "cms-salt-2026-v1";

    private final SecretKey secretKey;

    public SecurityServiceImpl() {
        this(DEFAULT_KEY, DEFAULT_SALT);
    }

    @Autowired
    public SecurityServiceImpl(
            @Value("${cms.security.aes-key:" + "CourseManagementSystemSecretKey2026}") String aesKey,
            @Value("${cms.security.aes-salt:" + "cms-salt-2026-v1}") String aesSalt) {
        try {
            this.secretKey = AESUtil.getKeyFromPassword(aesKey, aesSalt);
        } catch (Exception e) {
            throw new ExceptionInInitializerError("Could not initialize SecurityService SecretKey: " + e.getMessage());
        }
    }

    @Override
    public EncryptResponseDTO encrypt(EncryptRequestDTO request) {
        if (request == null || request.getData() == null) {
            throw new BadRequestException(MessageConstants.DATA_TO_ENCRYPT_CANNOT_BE_EMPTY);
        }
        try {
            logger.info("Encrypting sensitive payload of length {}", request.getData().length());
            String encrypted = AESUtil.encryptStringWithIv(request.getData(), this.secretKey);
            return EncryptResponseDTO.builder()
                    .encryptedData(encrypted)
                    .algorithm(AESUtil.DEFAULT_ALGORITHM)
                    .build();
        } catch (Exception e) {
            logger.error("Error during encryption: {}", e.getMessage(), e);
            throw new BadRequestException(String.format(MessageConstants.ENCRYPTION_FAILED, e.getMessage()));
        }
    }

    @Override
    public DecryptResponseDTO decrypt(DecryptRequestDTO request) {
        if (request == null || request.getEncryptedData() == null) {
            throw new BadRequestException(MessageConstants.DATA_TO_DECRYPT_CANNOT_BE_EMPTY);
        }
        try {
            logger.info("Decrypting payload of length {}", request.getEncryptedData().length());
            String decrypted = AESUtil.decryptStringWithIv(request.getEncryptedData(), this.secretKey);
            return DecryptResponseDTO.builder()
                    .decryptedData(decrypted)
                    .build();
        } catch (Exception e) {
            logger.error("Error during decryption: {}", e.getMessage(), e);
            throw new BadRequestException(String.format(MessageConstants.DECRYPTION_FAILED, e.getMessage()));
        }
    }
}
