package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.entity.Document;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DocumentRepository extends JpaRepository<Document, String>, JpaSpecificationExecutor<Document> {

    List<Document> findByAppIdAndDeletedFalse(String appId);

    List<Document> findByDeletedFalse();
}
