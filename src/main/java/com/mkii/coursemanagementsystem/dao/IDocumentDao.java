package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.domain.Page;

import java.util.List;

public interface IDocumentDao extends IPaginationSortingDao<String, Document> {

    Document save(Document document);

    Document update(Document document);

    void delete(String id);

    Document getById(String id);

    Document findByPk(String id);

    Document getDocumentName(String fileName, String appId);

    List<Document> getDocumentByAppId(String appId);

    List<Document> findByAppId(String appId);

    List<Document> getAllActive();

    List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId);

    Integer getDocCount(String query, String appId);

    Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction);
}
