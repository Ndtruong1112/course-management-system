package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Course;

import java.util.List;

public interface ICourseDao extends IPaginationSortingDao<Long, Course> {

    Course save(Course course);

    Course update(Course course);

    void delete(Long id);

    Course getById(Long id);

    Course getByTitle(String title);

    List<Course> getAll();

    List<Course> searchByTitle(String keyword);

    List<Course> findByPriceRange(Double minPrice, Double maxPrice);

    Integer getCount();
}
