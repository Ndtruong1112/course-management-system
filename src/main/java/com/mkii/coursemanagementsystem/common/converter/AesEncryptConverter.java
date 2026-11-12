package com.mkii.coursemanagementsystem.common.converter;

import com.mkii.coursemanagementsystem.util.AESUtil;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.crypto.SecretKey;

/**
 * JPA AttributeConverter that automatically encrypts sensitive Entity fields using AES
 * before writing to the database, and transparently decrypts them back upon retrieval.
 */
@Converter
public class AesEncryptConverter implements AttributeConverter<String, String> {

    private static final Logger logger = LoggerFactory.getLogger(AesEncryptConverter.class);
    private static final SecretKey SECRET_KEY;

    static {
        try {
            String key = System.getenv("CMS_AES_KEY") != null
                    ? System.getenv("CMS_AES_KEY") : "CourseManagementSystemSecretKey2026";
            String salt = System.getenv("CMS_AES_SALT") != null
                    ? System.getenv("CMS_AES_SALT") : "cms-salt-2026-v1";
            SECRET_KEY = AESUtil.getKeyFromPassword(key, salt);
        } catch (Exception e) {
            throw new ExceptionInInitializerError("Could not initialize AES SecretKey: " + e.getMessage());
        }
    }

    @Override
    public String convertToDatabaseColumn(String attribute) {
        if (attribute == null || attribute.trim().isEmpty()) {
            return attribute;
        }
        try {
            return AESUtil.encryptStringWithIv(attribute, SECRET_KEY);
        } catch (Exception e) {
            logger.error("Error encrypting entity attribute: {}", e.getMessage());
            return attribute;
        }
    }

    @Override
    public String convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.trim().isEmpty()) {
            return dbData;
        }
        try {
            return AESUtil.decryptStringWithIv(dbData, SECRET_KEY);
        } catch (Exception e) {
            // Graceful fallback for unencrypted legacy / mock data
            return dbData;
        }
    }
}
