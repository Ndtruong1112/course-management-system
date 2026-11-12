package com.mkii.coursemanagementsystem.dao;

import com.mkii.coursemanagementsystem.entity.Department;

import java.util.List;
import java.util.Optional;

public interface IDepartmentDao extends IPaginationSortingDao<Long, Department> {

    Department save(Department department);

    Department update(Department department);

    void delete(Long id);

    Department getById(Long id);

    Optional<Department> findByDepartmentCode(String departmentCode);

    List<Department> getAll();

    List<Department> searchByName(String keyword);

    Integer getCount();
}
