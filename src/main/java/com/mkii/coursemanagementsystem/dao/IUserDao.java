package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.User;

import java.util.List;
import java.util.Optional;

public interface IUserDao extends IPaginationSortingDao<Long, User> {

    User save(User user);

    User update(User user);

    void delete(Long id);

    User getById(Long id);

    Optional<User> findByUsername(String username);

    Optional<User> findByEmail(String email);

    boolean existsByUsername(String username);

    boolean existsByEmail(String email);

    List<User> getAll();

    Integer getCount();
}
