package com.mkii.coursemanagementsystem.dao;

import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Base Generic DAO interface defining standard CRUD and basic query operations.
 * Keeping this interface clean and focused purely on core entity persistence.
 */
public interface IGenericDao<Pk, Entity> {

    @Transactional
    Entity create(Entity anEntity);

    @Transactional
    Entity update(Entity anEntity);

    @Transactional
    Entity saveOrUpdate(Entity anEntity);

    @Transactional
    void delete(Entity anEntity);

    @Transactional
    void deleteById(Pk id);

    void deleteByPk(Pk id);

    Entity get(Pk id);

    Optional<Entity> findById(Pk id);

    Entity getByField(String fieldName, Object value);

    List<Entity> findByField(String fieldName, Object value);

    List<Entity> getAll();

    @Transactional
    List<Entity> createAll(List<Entity> entities);

    @Transactional
    void deleteAll(List<Entity> entities);

    boolean exists(Pk id);

    long count();

    void flush();

    void clear();
}
