package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

public interface DocumentRest {

    @PostMapping(value = {"/create", "/upload", ""}, consumes = "multipart/form-data")
    ResponseEntity<List<Document>> createDocument(
            @RequestParam("files") List<MultipartFile> files,
            @RequestParam("appId") String appId);

    @GetMapping("/download")
    ResponseEntity<byte[]> downloadDocumentByPath(@RequestParam("filePath") String filePath);

    @GetMapping("/download/{id}")
    ResponseEntity<byte[]> downloadDocumentById(@PathVariable String id);

    @PostMapping("/delete")
    ResponseEntity<String> deleteDocument(@RequestBody Map<String, String> id);

    @DeleteMapping("/{id}")
    ResponseEntity<String> deleteDocumentById(@PathVariable String id);

    @GetMapping("/{id}")
    ResponseEntity<Document> getDocumentById(@PathVariable String id);

    @GetMapping("/app/{appId}")
    ResponseEntity<List<Document>> getDocumentsByAppId(@PathVariable String appId);

    @GetMapping("/app/{appId}/paged")
    ResponseEntity<Page<Document>> getDocumentsByAppIdPaged(
            @PathVariable String appId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping(value = {"/list", ""})
    ResponseEntity<List<Document>> getAllActiveDocuments();

    @GetMapping("/paged")
    ResponseEntity<Page<Document>> getDocumentsPaged(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/sorted")
    ResponseEntity<List<Document>> getDocumentsSorted(
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);

    @GetMapping("/search")
    ResponseEntity<List<Document>> searchDocuments(
            @RequestParam(required = false) String query,
            @RequestParam(required = false, defaultValue = "0") Integer lowerLimit,
            @RequestParam(required = false, defaultValue = "10") Integer upperLimit,
            @RequestParam(required = false, defaultValue = "creationTime") String orderBy,
            @RequestParam(required = false, defaultValue = "desc") String orderType,
            @RequestParam(required = false) String appId);

    @GetMapping("/count")
    ResponseEntity<Integer> getDocCount(
            @RequestParam(required = false) String query,
            @RequestParam(required = false) String appId);

    @GetMapping("/spec-search-paged")
    ResponseEntity<Page<Document>> searchBySpecificationPaged(
            @RequestParam String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "creationTime") String sortBy,
            @RequestParam(defaultValue = "desc") String direction);
}
