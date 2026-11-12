package com.mkii.coursemanagementsystem.dao.impl;

import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.entity.User;
import com.mkii.coursemanagementsystem.hibernateDao.HibernatePaginationSortingDao;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.TypedQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public class UserDaoImpl extends HibernatePaginationSortingDao<Long, User> implements IUserDao {

    private static final Logger logger = LoggerFactory.getLogger(UserDaoImpl.class);

    public UserDaoImpl(EntityManager entityManager) {
        super(User.class, entityManager);
    }

    @Override
    public User save(User user) {
        logger.info("Saving User: {}", user.getUsername());
        return super.save(user);
    }

    @Override
    public User update(User user) {
        logger.info("Updating User: {}", user.getUserId());
        return super.update(user);
    }

    @Override
    public void delete(Long id) {
        logger.info("Deleting User: {}", id);
        deleteByPk(id);
    }

    @Override
    public User getById(Long id) {
        logger.info("Getting User by ID: {}", id);
        return get(id);
    }

    @Override
    public Optional<User> findByUsername(String username) {
        logger.info("Finding User by username: {}", username);
        String hql = "SELECT u FROM User u WHERE u.username = :username";
        TypedQuery<User> query = entityManager.createQuery(hql, User.class);
        query.setParameter("username", username);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public Optional<User> findByEmail(String email) {
        logger.info("Finding User by email: {}", email);
        String hql = "SELECT u FROM User u WHERE u.email = :email";
        TypedQuery<User> query = entityManager.createQuery(hql, User.class);
        query.setParameter("email", email);
        try {
            return Optional.of(query.getSingleResult());
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }

    @Override
    public boolean existsByUsername(String username) {
        String hql = "SELECT COUNT(u) FROM User u WHERE u.username = :username";
        TypedQuery<Long> query = entityManager.createQuery(hql, Long.class);
        query.setParameter("username", username);
        return query.getSingleResult() > 0;
    }

    @Override
    public boolean existsByEmail(String email) {
        String hql = "SELECT COUNT(u) FROM User u WHERE u.email = :email";
        TypedQuery<Long> query = entityManager.createQuery(hql, Long.class);
        query.setParameter("email", email);
        return query.getSingleResult() > 0;
    }

    @Override
    public List<User> getAll() {
        logger.info("Fetching all users");
        return findAll();
    }

    @Override
    public Integer getCount() {
        logger.info("Getting total users count");
        return (int) count();
    }
}
