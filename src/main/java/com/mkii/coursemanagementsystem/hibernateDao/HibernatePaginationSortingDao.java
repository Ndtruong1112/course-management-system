package com.mkii.coursemanagementsystem.hibernateDao;

import com.mkii.coursemanagementsystem.dao.IPaginationSortingDao;
import com.mkii.coursemanagementsystem.specification.GenericSpecificationsBuilder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.Collections;
import java.util.List;

/**
 * Specialized DAO implementation extending {@link HibernateGenericDao} that houses
 * all Sorting, Pagination, and Specification-based query logic.
 * Keeps HibernateGenericDao lean and modular.
 */
public class HibernatePaginationSortingDao<Pk, Entity> extends HibernateGenericDao<Pk, Entity> implements IPaginationSortingDao<Pk, Entity> {

    private static final Logger logger = LoggerFactory.getLogger(HibernatePaginationSortingDao.class);

    public HibernatePaginationSortingDao(Class<Entity> type, EntityManager entityManager) {
        super(type, entityManager);
    }

    // ──────────── Sorting / Pagination Methods ────────────

    @Override
    public List<Entity> findAllSorted(String sortBy, String direction) {
        logger.info("Finding all {} sorted by {} {}", getType().getSimpleName(), sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        return findAll(sort);
    }

    @Override
    public Page<Entity> findAllPaged(int page, int size, String sortBy, String direction) {
        logger.info("Finding all {} paged: page={}, size={}, sort={} {}", getType().getSimpleName(), page, size, sortBy, direction);
        Sort sort = buildSort(sortBy, direction);
        Pageable pageable = PageRequest.of(page, size, sort);
        return findAll(pageable);
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return Collections.emptyList();
        }
        logger.info("Finding {} by field {} = {} with sort {}", getType().getSimpleName(), fieldName, value, sort);
        try {
            String orderClause = buildOrderClause(sort);
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            TypedQuery<Entity> query = getEntityManager().createQuery(jpql, getType());
            query.setParameter("value", value);
            return query.getResultList();
        } catch (Exception e) {
            logger.error("Error finding {} by field {} sorted: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return Collections.emptyList();
        }
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable) {
        if (!isValidIdentifier(fieldName)) {
            logger.warn("Invalid field name: {}", fieldName);
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
        logger.info("Finding {} by field {} = {} paged: page={}, size={}", getType().getSimpleName(), fieldName, value, pageable.getPageNumber(), pageable.getPageSize());
        try {
            // Count query
            String countJpql = "SELECT COUNT(e) FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value";
            Long total = getEntityManager().createQuery(countJpql, Long.class)
                    .setParameter("value", value)
                    .getSingleResult();

            if (total == null || total == 0) {
                return new PageImpl<>(Collections.emptyList(), pageable, 0);
            }

            // Data query with order and pagination
            String orderClause = buildOrderClause(pageable.getSort());
            String jpql = "SELECT e FROM " + getType().getSimpleName()
                    + " e WHERE e." + fieldName + " = :value" + orderClause;
            List<Entity> content = getEntityManager().createQuery(jpql, getType())
                    .setParameter("value", value)
                    .setFirstResult((int) pageable.getOffset())
                    .setMaxResults(pageable.getPageSize())
                    .getResultList();

            return new PageImpl<>(content, pageable, total);
        } catch (Exception e) {
            logger.error("Error finding {} by field {} paged: {}", getType().getSimpleName(), fieldName, e.getMessage());
            return new PageImpl<>(Collections.emptyList(), pageable, 0);
        }
    }

    @Override
    public List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction) {
        return findByFieldSorted(fieldName, value, buildSort(sortBy, direction));
    }

    @Override
    public Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction) {
        Pageable pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return findByFieldPaged(fieldName, value, pageable);
    }

    // ──────────── Specification Search Methods ────────────

    @Override
    public List<Entity> searchBySpecification(String search) {
        logger.info("Searching {} by Specification query: {}", getType().getSimpleName(), search);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        return (spec == null) ? getAll() : findAll(spec);
    }

    @Override
    public List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction) {
        logger.info("Searching {} by spec sorted: search={}, sort={} {}", getType().getSimpleName(), search, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        Sort sort = buildSort(sortBy, direction);
        return (spec == null) ? findAllSorted(sortBy, direction) : findAll(spec, sort);
    }

    @Override
    public Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction) {
        logger.info("Searching {} by spec paged: search={}, page={}, size={}, sort={} {}", getType().getSimpleName(), search, page, size, sortBy, direction);
        GenericSpecificationsBuilder<Entity> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery(search);
        Specification<Entity> spec = builder.build();
        PageRequest pageable = PageRequest.of(page, size, buildSort(sortBy, direction));
        return (spec == null) ? getAll(pageable) : findAll(spec, pageable);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec, Sort sort) {
        return super.findAll(spec, sort);
    }

    @Override
    public List<Entity> findAll(Specification<Entity> spec) {
        return super.findAll(spec);
    }

    @Override
    public Page<Entity> findAll(Specification<Entity> spec, Pageable pageable) {
        return super.findAll(spec, pageable);
    }

    @Override
    public Page<Entity> getAll(Pageable pageable) {
        return findAll(pageable);
    }

    @Override
    public List<Entity> getAll(Sort sort) {
        return findAll(sort);
    }

    // ──────────── Helper Methods ────────────

    protected Sort buildSort(String sortBy, String direction) {
        if (sortBy == null || sortBy.isBlank() || !isValidIdentifier(sortBy)) {
            return Sort.unsorted();
        }
        return "desc".equalsIgnoreCase(direction)
                ? Sort.by(sortBy).descending()
                : Sort.by(sortBy).ascending();
    }

    protected String buildOrderClause(Sort sort) {
        if (sort == null || sort.isUnsorted()) {
            return "";
        }
        StringBuilder sb = new StringBuilder(" ORDER BY ");
        boolean hasOrder = false;
        for (Sort.Order order : sort) {
            if (isValidIdentifier(order.getProperty())) {
                sb.append("e.")
                        .append(order.getProperty())
                        .append(" ")
                        .append(order.getDirection().name())
                        .append(", ");
                hasOrder = true;
            }
        }
        return hasOrder ? sb.substring(0, sb.length() - 2) : "";
    }
}
