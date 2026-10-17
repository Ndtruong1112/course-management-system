package com.mkii.coursemanagementsystem.service.impl;

import com.mkii.coursemanagementsystem.common.MessageConstants;
import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.service.DocumentService;
import com.mkii.coursemanagementsystem.service.MinioStorageService;
import org.apache.commons.io.FilenameUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
@Transactional
public class DocumentServiceImpl implements DocumentService {

    private static final Logger logger = LoggerFactory.getLogger(DocumentServiceImpl.class);

    private static final String[] SUPPORTED_EXTENSIONS = {
            "pdf", "xlsx", "xls", "doc", "docx", "jpg", "jpeg", "png"
    };

    // Strict architectural compliance: call ONLY IDocumentDao interface
    @Autowired
    private IDocumentDao documentDao;

    @Autowired
    private MinioStorageService minioStorageService;

    @Override
    @Transactional
    public List<Document> create(List<MultipartFile> files, String appId) {
        logger.info("Starting document creation for appId: {}, total files: {}", appId, files != null ? files.size() : 0);

        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId (mã công việc/nghiệp vụ) không được để trống.");
        }
        if (files == null || files.isEmpty()) {
            throw new BadRequestException("Danh sách file tải lên không hợp lệ hoặc để trống.");
        }

        List<Document> documentList = new ArrayList<>();

        for (MultipartFile file : files) {
            if (file != null && !file.isEmpty() && file.getOriginalFilename() != null && !file.getOriginalFilename().trim().isEmpty()) {
                String originalFilename = FilenameUtils.getName(file.getOriginalFilename());

                // 1. Kiểm tra ký tự đặc biệt trong tên file
                if (!checkFileNameSpecialChar(originalFilename)) {
                    throw new BadRequestException("Tên file không được chứa ký tự đặc biệt: " + originalFilename);
                }

                // 2. Kiểm tra độ dài tên file (phần trước dấu chấm <= 50 ký tự)
                String baseName = FilenameUtils.getBaseName(originalFilename);
                if (baseName.length() > 50) {
                    throw new BadRequestException("Tên file vượt quá độ dài tối đa 50 ký tự: " + baseName);
                }

                // 3. Kiểm tra định dạng đuôi file
                InputStream inputStream = validateFileExtension(file);

                String extension = FilenameUtils.getExtension(originalFilename);
                String storagePath = appId + "/" + UUID.randomUUID() + (extension.isEmpty() ? "" : "." + extension);

                // 4. Lưu trữ file lên MinIO
                minioStorageService.upload(storagePath, inputStream, file.getContentType(), file.getSize());

                // 5. Kiểm tra tài liệu cùng tên đã tồn tại cho appId này chưa (Versioning logic)
                Document documentDetail = documentDao.getDocumentName(originalFilename, appId);
                if (documentDetail == null) {
                    Document docData = createDocument(originalFilename, appId, storagePath);
                    documentList.add(docData);
                } else {
                    logger.info("Tài liệu '{}' đã tồn tại, tạo phiên bản mới", documentDetail.getName());
                    Document docDataWithNewVersion = createDocumentWithNewVersion(originalFilename, appId, storagePath, documentDetail);
                    documentList.add(docDataWithNewVersion);
                }
            } else {
                throw new BadRequestException("File tải lên không được để trống.");
            }
        }

        return documentList;
    }

    @Override
    public Document createDocument(String fileName, String appId, String fileobj) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);
        doc.setVersion(1.0);
        return documentDao.save(doc);
    }

    @Override
    public Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail) {
        Document doc = new Document();
        setDocumentDetails(fileName, appId, fileobj, doc);

        // Vô hiệu hóa phiên bản cũ
        if (Boolean.TRUE.equals(documentDetail.getActive())) {
            documentDetail.setActive(false);
            documentDao.update(documentDetail);
        }

        // Tăng số phiên bản cho tài liệu mới
        Double versionCount = documentDetail.getVersion() != null ? documentDetail.getVersion() : 1.0;
        doc.setVersion(++versionCount);
        return documentDao.save(doc);
    }

    private void setDocumentDetails(String fileName, String appId, String fileobj, Document doc) {
        doc.setAppId(appId);
        doc.setName(fileName);
        doc.setPath(fileobj);
        doc.setOwner("SYSTEM");
        doc.setDeleted(false);
        doc.setActive(true);
    }

    public static boolean checkFileNameSpecialChar(String fileName) {
        if (fileName == null || fileName.isBlank()) {
            return false;
        }
        return fileName.matches("^[a-zA-Z0-9._\\s\\p{L}-]+$");
    }

    @Override
    public ResponseEntity<byte[]> download(String filePath) {
        logger.info("Downloading document by filePath: {}", filePath);
        if (filePath == null || filePath.trim().isEmpty()) {
            throw new BadRequestException("Đường dẫn file không được để trống.");
        }

        byte[] data = minioStorageService.download(filePath);
        String filename = FilenameUtils.getName(filePath);
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public ResponseEntity<byte[]> downloadById(String id) {
        logger.info("Downloading document by id: {}", id);
        Document document = getById(id);
        byte[] data = minioStorageService.download(document.getPath());

        String filename = document.getName() != null ? document.getName() : FilenameUtils.getName(document.getPath());
        String encodedFilename = URLEncoder.encode(filename, StandardCharsets.UTF_8).replace("+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFilename + "\"")
                .body(data);
    }

    @Override
    public String delete(Map<String, String> id) {
        Document document = fetchAndValidateDocumentById(id);
        logger.info("Soft deleting document name: {}, id: {}", document.getName(), document.getId());
        document.setDeleted(true);
        document.setActive(false);
        documentDao.update(document);
        return MessageConstants.SUCCESS_JSON;
    }

    @Override
    public String deleteById(String id) {
        return delete(Map.of("id", id));
    }

    @Override
    public Document fetchAndValidateDocumentById(Map<String, String> id) {
        if (id == null) {
            throw new BadRequestException(MessageConstants.INVALID_DOCUMENT);
        }
        String docId = id.get("id");
        if (docId == null) {
            docId = id.get("ID");
        }
        if (docId != null && !docId.trim().isEmpty()) {
            Document document = documentDao.findByPk(docId.trim());
            if (document != null && !Boolean.TRUE.equals(document.getDeleted())) {
                return document;
            }
        }
        throw new ResourceNotFoundException(MessageConstants.INVALID_DOCUMENT);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting document by id: {}", id);
        Document document = documentDao.findByPk(id);
        if (document == null || Boolean.TRUE.equals(document.getDeleted())) {
            throw new ResourceNotFoundException(String.format(MessageConstants.DOCUMENT_NOT_FOUND, id));
        }
        return document;
    }

    @Override
    public List<Document> getByAppId(String appId) {
        logger.info("Getting documents for appId: {}", appId);
        if (appId == null || appId.trim().isEmpty()) {
            throw new BadRequestException("appId không được để trống.");
        }
        return documentDao.getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active documents");
        return documentDao.getAllActive();
    }

    // ──────────── Pagination, Sorting & Search (Delegated to IDocumentDao) ────────────

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("Service getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);
        return documentDao.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("Service getDocCount: query={}, appId={}", query, appId);
        return documentDao.getDocCount(query, appId);
    }

    @Override
    public Page<Document> getAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Service getAllPaged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
        return documentDao.findAllPaged(page, size, sortBy, direction);
    }

    @Override
    public List<Document> getAllSorted(String sortBy, String direction) {
        logger.info("Service getAllSorted: sort={} {}", sortBy, direction);
        return documentDao.findAllSorted(sortBy, direction);
    }

    @Override
    public Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("Service getByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        return documentDao.findByAppIdPaged(appId, page, size, sortBy, direction);
    }

    @Override
    public Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Service searchBySpecificationPaged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
        return documentDao.searchBySpecificationPaged(search, page, size, sortBy, direction);
    }

    // ──────────── Private helper methods ────────────

    private InputStream validateFileExtension(MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null) {
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }

        String extension = FilenameUtils.getExtension(originalFilename).toLowerCase();
        logger.info("Validating extension from multipart: '{}'", extension);

        if (Arrays.asList(SUPPORTED_EXTENSIONS).contains(extension)) {
            try {
                return file.getInputStream();
            } catch (IOException e) {
                logger.error("Error reading file input stream: {}", e.getMessage(), e);
                throw new BadRequestException("Không thể đọc dữ liệu file: " + e.getMessage());
            }
        } else {
            logger.warn("File extension '{}' is not supported", extension);
            throw new BadRequestException(MessageConstants.FILE_EXTENSION_NOT_SUPPORTED);
        }
    }
}
