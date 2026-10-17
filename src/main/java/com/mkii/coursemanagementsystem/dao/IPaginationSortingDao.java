package com.mkii.coursemanagementsystem.dao;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

import java.util.List;

/**
 * Interface extending {@link IGenericDao} dedicated to Sorting, Pagination,
 * and Dynamic Specification Search.
 */
public interface IPaginationSortingDao<Pk, Entity> extends IGenericDao<Pk, Entity> {

    /** Get all records sorted by a field name and direction ("asc" / "desc"). */
    List<Entity> findAllSorted(String sortBy, String direction);

    /** Get a single page of records, sorted. */
    Page<Entity> findAllPaged(int page, int size, String sortBy, String direction);

    /** Find all records matching a field value, applying Sort. */
    List<Entity> findByFieldSorted(String fieldName, Object value, Sort sort);

    /** Find all records matching a field value, sorted by string parameters. */
    List<Entity> findByFieldSorted(String fieldName, Object value, String sortBy, String direction);

    /** Find all records matching a field value, with full Pageable (page + size + sort). */
    Page<Entity> findByFieldPaged(String fieldName, Object value, Pageable pageable);

    /** Find all records matching a field value with pagination and sorting via string parameters. */
    Page<Entity> findByFieldPaged(String fieldName, Object value, int page, int size, String sortBy, String direction);

    /** Search by query string (key:op:value) using Specification. */
    List<Entity> searchBySpecification(String search);

    /** Search by query string using Specification combined with sorting. */
    List<Entity> searchBySpecificationSorted(String search, String sortBy, String direction);

    /** Search by query string using Specification combined with pagination and sorting. */
    Page<Entity> searchBySpecificationPaged(String search, int page, int size, String sortBy, String direction);

    /** Raw Spring Data Specification search without paging. */
    List<Entity> findAll(Specification<Entity> spec);

    /** Raw Spring Data Specification search with paging. */
    Page<Entity> findAll(Specification<Entity> spec, Pageable pageable);

    /** Raw Spring Data Specification search with sort. */
    List<Entity> findAll(Specification<Entity> spec, Sort sort);

    Page<Entity> getAll(Pageable pageable);

    List<Entity> getAll(Sort sort);
}
