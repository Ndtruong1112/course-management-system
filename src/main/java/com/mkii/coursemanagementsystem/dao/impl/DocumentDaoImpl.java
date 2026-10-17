package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class DocumentDaoImpl extends HibernatePaginationSortingDao<String, Document> implements IDocumentDao {

    private static final Logger logger = LoggerFactory.getLogger(DocumentDaoImpl.class);

    public DocumentDaoImpl(EntityManager entityManager) {
        super(Document.class, entityManager);
    }

    @Override
    public Document save(Document document) {
        logger.info("Saving Document: name={}, appId={}", document.getName(), document.getAppId());
        return create(document);
    }

    @Override
    public Document update(Document document) {
        logger.info("Updating Document: id={}", document.getId());
        return super.update(document);
    }

    @Override
    public void delete(String id) {
        logger.info("Deleting Document: id={}", id);
        deleteByPk(id);
    }

    @Override
    public Document getById(String id) {
        logger.info("Getting Document by id: {}", id);
        return get(id);
    }

    @Override
    public Document findByPk(String id) {
        logger.info("Finding Document by pk: {}", id);
        return get(id);
    }

    @Override
    public Document getDocumentName(String fileName, String appId) {
        logger.info("document name: {} for appId: {}", fileName, appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByName", Document.class)
                    .setParameter("name", fileName)
                    .setParameter("appId", appId);
            List<Document> list = query.setMaxResults(1).getResultList();
            return list.isEmpty() ? null : list.get(0);
        } catch (Exception e) {
            logger.error("Error executing getDocumentByName: {}", e.getMessage());
            return null;
        }
    }

    @Override
    public List<Document> getDocumentByAppId(String appId) {
        logger.info("Inside getDocumentByAppId appId: {}", appId);
        try {
            TypedQuery<Document> query = getEntityManager()
                    .createNamedQuery("getDocumentByAppId", Document.class)
                    .setParameter("appId", appId);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error executing getDocumentByAppId: {}", e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public List<Document> findByAppId(String appId) {
        return getDocumentByAppId(appId);
    }

    @Override
    public List<Document> getAllActive() {
        logger.info("Getting all active Documents");
        return findByHql(
                "SELECT d FROM Document d WHERE d.deleted = false ORDER BY d.creationTime DESC",
                null
        );
    }

    @Override
    public List<Document> getDoc(String query, Integer lowerLimit, Integer upperLimit, String orderBy, String orderType, String appId) {
        logger.info("getDoc: query={}, lowerLimit={}, upperLimit={}, orderBy={}, orderType={}, appId={}",
                query, lowerLimit, upperLimit, orderBy, orderType, appId);

        int offset = (lowerLimit != null && lowerLimit >= 0) ? lowerLimit : 0;
        int limit = (upperLimit != null && upperLimit > 0) ? upperLimit : 10;
        String sortField = (orderBy != null && !orderBy.isBlank()) ? orderBy : "creationTime";
        String direction = (orderType != null && !orderType.isBlank()) ? orderType : "desc";

        StringBuilder jpql = new StringBuilder("SELECT d FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        Sort sort = buildSort(sortField, direction);
        jpql.append(buildOrderClause(sort));

        TypedQuery<Document> typedQuery = getEntityManager().createQuery(jpql.toString(), Document.class);
        params.forEach(typedQuery::setParameter);
        typedQuery.setFirstResult(offset);
        typedQuery.setMaxResults(limit);

        return typedQuery.getResultList();
    }

    @Override
    public Integer getDocCount(String query, String appId) {
        logger.info("getDocCount: query={}, appId={}", query, appId);

        StringBuilder jpql = new StringBuilder("SELECT COUNT(d) FROM Document d WHERE d.deleted = false");
        Map<String, Object> params = new HashMap<>();

        if (appId != null && !appId.isBlank()) {
            jpql.append(" AND d.appId = :appId");
            params.put("appId", appId);
        }

        if (query != null && !query.isBlank()) {
            jpql.append(" AND LOWER(d.name) LIKE LOWER(:query)");
            params.put("query", "%" + query.trim() + "%");
        }

        TypedQuery<Long> countQuery = getEntityManager().createQuery(jpql.toString(), Long.class);
        params.forEach(countQuery::setParameter);

        Long count = countQuery.getSingleResult();
        return count != null ? count.intValue() : 0;
    }

    @Override
    public Page<Document> findByAppIdPaged(String appId, int page, int size, String sortBy, String direction) {
        logger.info("findByAppIdPaged: appId={}, page={}, size={}, sort={} {}", appId, page, size, sortBy, direction);
        return findByFieldPaged("appId", appId, page, size, sortBy, direction);
    }
}
