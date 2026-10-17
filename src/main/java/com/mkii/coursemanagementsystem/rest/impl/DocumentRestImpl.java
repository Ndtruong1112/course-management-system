package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.rest.DocumentRest;
import com.mkii.coursemanagementsystem.service.DocumentService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping(ApiConstants.BASE_DOCUMENT_URL)
@CrossOrigin(origins = "*", maxAge = 3600)
public class DocumentRestImpl implements DocumentRest {

    private static final Logger logger = LoggerFactory.getLogger(DocumentRestImpl.class);

    @Autowired
    private DocumentService documentService;

    @Override
    public ResponseEntity<List<Document>> createDocument(List<MultipartFile> files, String appId) {
        try {
            logger.info("REST: Creating documents for appId: {}, total files: {}", appId, files != null ? files.size() : 0);
            List<Document> documents = documentService.create(files, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error creating documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentByPath(String filePath) {
        try {
            logger.info("REST: Downloading document by filePath: {}", filePath);
            return documentService.download(filePath);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by path: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<byte[]> downloadDocumentById(String id) {
        try {
            logger.info("REST: Downloading document by id: {}", id);
            return documentService.downloadById(id);
        } catch (Exception e) {
            logger.error("REST: Error downloading document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocument(Map<String, String> id) {
        try {
            logger.info("REST: Deleting document with request body: {}", id);
            String result = documentService.delete(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<String> deleteDocumentById(String id) {
        try {
            logger.info("REST: Deleting document by id: {}", id);
            String result = documentService.deleteById(id);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.error("REST: Error deleting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Document> getDocumentById(String id) {
        try {
            logger.info("REST: Getting document by id: {}", id);
            Document document = documentService.getById(id);
            return ResponseEntity.ok(document);
        } catch (Exception e) {
            logger.error("REST: Error getting document by id: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsByAppId(String appId) {
        try {
            logger.info("REST: Getting documents for appId: {}", appId);
            List<Document> documents = documentService.getByAppId(appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents for appId: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents for appId: {} paged: page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
            Page<Document> documents = documentService.getByAppIdPaged(appId, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents by appId paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getAllActiveDocuments() {
        try {
            logger.info("REST: Getting all active documents");
            List<Document> documents = documentService.getAllActive();
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting all documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> getDocumentsPaged(int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents paged: page={}, size={}, sort={} {}", page, size, sortBy, direction);
            Page<Document> documents = documentService.getAllPaged(page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents paged: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> getDocumentsSorted(String sortBy, String direction) {
        try {
            logger.info("REST: Getting documents sorted: sort={} {}", sortBy, direction);
            List<Document> documents = documentService.getAllSorted(sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error getting documents sorted: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<List<Document>> searchDocuments(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        try {
            logger.info("REST: Searching documents: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                    query, lowerLimit, upperLimit, orderBy, orderType, appId);
            List<Document> documents = documentService.getDoc(query, lowerLimit, upperLimit, orderBy, orderType, appId);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Integer> getDocCount(String query, String appId) {
        try {
            logger.info("REST: Getting document count: query={}, appId={}", query, appId);
            Integer count = documentService.getDocCount(query, appId);
            return ResponseEntity.ok(count);
        } catch (Exception e) {
            logger.error("REST: Error getting document count: ", e);
            throw e;
        }
    }

    @Override
    public ResponseEntity<Page<Document>> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        try {
            logger.info("REST: Searching documents by spec paged: search={}, page={}, size={}, sort={} {}", search, page, size, sortBy, direction);
            Page<Document> documents = documentService.searchBySpecificationPaged(search, page, size, sortBy, direction);
            return ResponseEntity.ok(documents);
        } catch (Exception e) {
            logger.error("REST: Error searching documents by spec paged: ", e);
            throw e;
        }
    }
}
