package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;
import java.util.UUID;

@NamedQuery(
        name = "getDocumentByName",
        query = "SELECT d FROM Document d WHERE d.name = :name AND d.deleted = false AND d.active = true AND d.appId = :appId"
)
@NamedQuery(
        name = "getDocumentByAppId",
        query = "SELECT d FROM Document d WHERE d.appId = :appId AND d.deleted = false ORDER BY d.creationTime DESC"
)
@Entity
@Table(name = "documents", indexes = {
        @Index(name = "idx_doc_app_id", columnList = "APP_DETAIL_FK"),
        @Index(name = "idx_doc_name", columnList = "NAME"),
        @Index(name = "idx_doc_deleted", columnList = "DELETED"),
        @Index(name = "idx_doc_active", columnList = "ACTIVE")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Document {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "ID", updatable = false, nullable = false, length = 36)
    @EqualsAndHashCode.Include
    private String id;

    @Column(name = "APP_DETAIL_FK", nullable = false)
    private String appId;

    @Column(name = "NAME")
    private String name;

    @Column(name = "PATH")
    private String path;

    @Column(name = "OWNER")
    private String owner;

    @Column(name = "VERSION")
    private Double version;

    @Column(name = "DELETED")
    private Boolean deleted;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "CREATED_TIME")
    private Date creationTime;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "MODIFIED_TIME")
    private Date modificationTime;

    @Column(name = "ACTIVE")
    private Boolean active;

    @PrePersist
    void onCreate() {
        if (this.id == null || this.id.isBlank()) {
            this.id = UUID.randomUUID().toString();
        }
        Date now = new Date();
        this.creationTime = now;
        this.modificationTime = now;
        if (this.deleted == null) {
            this.deleted = false;
        }
        if (this.active == null) {
            this.active = true;
        }
        if (this.version == null) {
            this.version = 1.0;
        }
    }

    @PreUpdate
    void onPersist() {
        this.modificationTime = new Date();
    }
}
