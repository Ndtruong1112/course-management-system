package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IStudentDao;
import com.mkii.coursemanagementsystem.entity.Student;
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
public class StudentDaoImpl extends HibernatePaginationSortingDao<Long, Student> implements IStudentDao {

    private static final Logger logger = LoggerFactory.getLogger(StudentDaoImpl.class);

    public StudentDaoImpl(EntityManager entityManager) {
        super(Student.class, entityManager);
    }

    @Override
    public Student save(Student student) {
        logger.info("Saving Student: {}", student.getFullName());
        return create(student);
    }

    @Override
    public Student update(Student student) {
        logger.info("Updating Student: {}", student.getId());
        return super.update(student);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Student: {}", id);
        deleteByPk(id);
    }

    @Override
    public Student getById(Long id) {
        logger.info("Getting Student by id: {}", id);
        return get(id);
    }

    @Override
    public Student getByEmail(String email) {
        logger.info("Getting Student by email: {}", email);
        return getByField("email", email);
    }

    @Override
    public Optional<Student> findByEmail(String email) {
        logger.info("Getting Student optional by email: {}", email);
        return Optional.ofNullable(getByField("email", email));
    }

    @Override
    public List<Student> getAll() {
        logger.info("Getting all Students");
        return findAll(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "id"));
    }

    @Override
    public List<Student> searchByKeyword(String keyword) {
        logger.info("Searching Students by keyword: {}", keyword);
        return findByHql(
                "SELECT s FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :keyword, '%'))",
                java.util.Map.of("keyword", keyword)
        );
    }

    @Override
    public Integer getCount() {
        logger.info("Getting Student count");
        return (int) count();
    }
}
