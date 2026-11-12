package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IDepartmentDao;
import com.mkii.coursemanagementsystem.entity.Department;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Repository
public class DepartmentDaoImpl extends HibernatePaginationSortingDao<Long, Department> implements IDepartmentDao {

    private static final Logger logger = LoggerFactory.getLogger(DepartmentDaoImpl.class);

    public DepartmentDaoImpl(EntityManager entityManager) {
        super(Department.class, entityManager);
    }

    @Override
    public Department save(Department department) {
        logger.info("Saving Department: {}", department.getDepartmentCode());
        return super.save(department);
    }

    @Override
    public Department update(Department department) {
        logger.info("Updating Department: {}", department.getDepartmentId());
        return super.update(department);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Department: {}", id);
        deleteByPk(id);
    }

    @Override
    public Department getById(Long id) {
        logger.info("Getting Department by ID: {}", id);
        return get(id);
    }

    @Override
    public Optional<Department> findByDepartmentCode(String departmentCode) {
        logger.info("Finding Department by code: {}", departmentCode);
        String hql = "SELECT d FROM Department d WHERE d.departmentCode = :code";
        TypedQuery<Department> query = entityManager.createQuery(hql, Department.class);
        query.setParameter("code", departmentCode);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public List<Department> getAll() {
        logger.info("Fetching all departments");
        return findAll();
    }

    @Override
    public List<Department> searchByName(String keyword) {
        logger.info("Searching departments by keyword: {}", keyword);
        if (keyword == null || keyword.trim().isEmpty()) {
            return Collections.emptyList();
        }
        String hql = "SELECT d FROM Department d WHERE LOWER(d.departmentName) LIKE LOWER(:keyword) OR LOWER(d.departmentCode) LIKE LOWER(:keyword)";
        TypedQuery<Department> query = entityManager.createQuery(hql, Department.class);
        query.setParameter("keyword", "%" + keyword.trim() + "%");
        return query.getResultList();
    }

    @Override
    public Integer getCount() {
        logger.info("Getting total departments count");
        return (int) count();
    }
}
