package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Student;

import java.util.List;
import java.util.Optional;

public interface IStudentDao extends IPaginationSortingDao<Long, Student> {

    Student save(Student student);

    Student update(Student student);

    void delete(Long id);

    Student getById(Long id);

    Student getByEmail(String email);

    Optional<Student> findByEmail(String email);

    List<Student> getAll();

    List<Student> searchByKeyword(String keyword);

    Integer getCount();
}
