package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentService {

    List<Document> create(List<MultipartFile> files, String appId);

    Document createDocument(String fileName, String appId, String fileobj);

    Document createDocumentWithNewVersion(String fileName, String appId, String fileobj, Document documentDetail);

    ResponseEntity<byte[]> download(String filePath);

    ResponseEntity<byte[]> downloadById(String id);

    String delete(Map<String, String> id);

    String deleteById(String id);

    Document fetchAndValidateDocumentById(Map<String, String> id);

    Document getById(String id);

    List<Document> getByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> getAllPaged(int page, int size, String sortBy, String direction);

    List<Document> getAllSorted(String sortBy, String direction);

    Page<Document> getByAppIdPaged(String appId, int page, int size, String sortBy, String direction);

    Page<Document> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);
}
