package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.entity.Enrollment;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Repository
public class EnrollmentDaoImpl extends HibernatePaginationSortingDao<Long, Enrollment> implements IEnrollmentDao {

    private static final Logger logger = LoggerFactory.getLogger(EnrollmentDaoImpl.class);

    public EnrollmentDaoImpl(EntityManager entityManager) {
        super(Enrollment.class, entityManager);
    }

    @Override
    public Enrollment save(Enrollment enrollment) {
        logger.info("Saving Enrollment for student={}, course={}",
                enrollment.getStudent() != null ? enrollment.getStudent().getId() : null,
                enrollment.getCourse() != null ? enrollment.getCourse().getId() : null);
        return super.save(enrollment);
    }

    @Override
    public Enrollment update(Enrollment enrollment) {
        logger.info("Updating Enrollment id={}", enrollment.getId());
        return super.update(enrollment);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting Enrollment id={}", id);
        deleteByPk(id);
    }

    @Override
    public Enrollment getById(Long id) {
        return get(id);
    }

    @Override
    public List<Enrollment> getAll() {
        return findAll();
    }

    @Override
    public boolean existsByStudentAndCourse(Long studentId, Long courseId) {
        String hql = "SELECT COUNT(e) FROM Enrollment e WHERE e.student.id = :studentId AND e.course.id = :courseId";
        Long cnt = getEntityManager().createQuery(hql, Long.class)
                .setParameter("studentId", studentId)
                .setParameter("courseId", courseId)
                .getSingleResult();
        return cnt != null && cnt > 0;
    }

    @Override
    public List<Enrollment> findByStudentId(Long studentId) {
        String hql = "SELECT e FROM Enrollment e WHERE e.student.id = :studentId ORDER BY e.enrolledAt DESC";
        return getEntityManager().createQuery(hql, Enrollment.class)
                .setParameter("studentId", studentId)
                .getResultList();
    }

    @Override
    public List<Enrollment> findByCourseId(Long courseId) {
        String hql = "SELECT e FROM Enrollment e WHERE e.course.id = :courseId ORDER BY e.enrolledAt DESC";
        return getEntityManager().createQuery(hql, Enrollment.class)
                .setParameter("courseId", courseId)
                .getResultList();
    }

    @Override
    public List<Enrollment> searchByKeyword(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return findAll();
        }
        String hql = "SELECT e FROM Enrollment e "
                + "WHERE LOWER(e.student.fullName) LIKE LOWER(:kw) "
                + "OR LOWER(e.student.email) LIKE LOWER(:kw) "
                + "OR LOWER(e.course.title) LIKE LOWER(:kw) "
                + "OR LOWER(e.status) LIKE LOWER(:kw) "
                + "ORDER BY e.enrolledAt DESC";
        TypedQuery<Enrollment> query = getEntityManager().createQuery(hql, Enrollment.class);
        query.setParameter("kw", "%" + keyword.trim() + "%");
        return query.getResultList();
    }

    @Override
    public Map<String, Long> countGroupByStatus() {
        String hql = "SELECT e.status, COUNT(e) FROM Enrollment e GROUP BY e.status";
        List<Object[]> rows = getEntityManager().createQuery(hql, Object[].class).getResultList();
        Map<String, Long> result = new LinkedHashMap<>();
        result.put("ENROLLED", 0L);
        result.put("COMPLETED", 0L);
        result.put("DROPPED", 0L);
        for (Object[] row : rows) {
            if (row != null && row[0] != null) {
                result.put(String.valueOf(row[0]), ((Number) row[1]).longValue());
            }
        }
        return result;
    }

    @Override
    public Double sumEnrolledCourseRevenue() {
        String hql = "SELECT COALESCE(SUM(e.course.price), 0) FROM Enrollment e WHERE e.status <> 'DROPPED'";
        Double sum = getEntityManager().createQuery(hql, Double.class).getSingleResult();
        return sum != null ? sum : 0.0;
    }

    @Override
    public Integer getCount() {
        return (int) count();
    }
}
