package com.mkii.coursemanagementsystem.service;

import io.minio.BucketExistsArgs;
import io.minio.GetObjectArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.InputStream;

@Service
public class MinioStorageService {

    private static final Logger logger = LoggerFactory.getLogger(MinioStorageService.class);

    @Autowired
    private MinioClient minioClient;

    @Value("${minio.bucket-name:documents}")
    private String bucketName;

    public void ensureBucketExists() {
        try {
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
            if (!exists) {
                logger.info("MinIO bucket '{}' does not exist. Creating bucket...", bucketName);
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
            }
        } catch (Exception e) {
            logger.error("Error verifying/creating MinIO bucket '{}': {}", bucketName, e.getMessage());
            throw new RuntimeException("Could not connect to MinIO storage: " + e.getMessage(), e);
        }
    }

    public void upload(String objectPath, InputStream inputStream, String contentType, long size) {
        ensureBucketExists();
        try {
            logger.info("Uploading object '{}' to MinIO bucket '{}' (size: {} bytes)", objectPath, bucketName, size);
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .stream(inputStream, size, -1)
                            .contentType(contentType != null ? contentType : "application/octet-stream")
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error uploading object '{}' to MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to upload file to MinIO: " + e.getMessage(), e);
        }
    }

    public byte[] download(String objectPath) {
        try {
            logger.info("Downloading object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            try (InputStream stream = minioClient.getObject(
                    GetObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build())) {
                return IOUtils.toByteArray(stream);
            }
        } catch (Exception e) {
            logger.error("Error downloading object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to download file from MinIO: " + e.getMessage(), e);
        }
    }

    public void delete(String objectPath) {
        try {
            logger.info("Removing object '{}' from MinIO bucket '{}'", objectPath, bucketName);
            minioClient.removeObject(
                    RemoveObjectArgs.builder()
                            .bucket(bucketName)
                            .object(objectPath)
                            .build()
            );
        } catch (Exception e) {
            logger.error("Error deleting object '{}' from MinIO: {}", objectPath, e.getMessage());
            throw new RuntimeException("Failed to delete file from MinIO: " + e.getMessage(), e);
        }
    }
}
