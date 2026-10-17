package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.dto.CourseResponseDTO;
import com.mkii.coursemanagementsystem.entity.Course;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CourseRepository extends JpaRepository<Course, Long>, JpaSpecificationExecutor<Course> {

    // Query 1: Tìm kiếm khóa học theo tên (Search title gần đúng) và map thẳng ra DTO
    @Query("SELECT new com.mkii.coursemanagementsystem.dto.CourseResponseDTO(c.id, c.title, c.description, c.duration, c.price) " +
            "FROM Course c WHERE LOWER(c.title) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<CourseResponseDTO> searchByTitle(@Param("keyword") String keyword);

    // Query 2: Lọc danh sách khóa học theo khoảng giá (Price range)
    @Query("SELECT new com.mkii.coursemanagementsystem.dto.CourseResponseDTO(c.id, c.title, c.description, c.duration, c.price) " +
            "FROM Course c WHERE c.price BETWEEN :minPrice AND :maxPrice")
    List<CourseResponseDTO> findByPriceRange(@Param("minPrice") Double minPrice, @Param("maxPrice") Double maxPrice);
}