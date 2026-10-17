package com.mkii.coursemanagementsystem.repository;

import com.mkii.coursemanagementsystem.dto.StudentResponseDTO;
import com.mkii.coursemanagementsystem.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Long>, JpaSpecificationExecutor<Student> {

    Optional<Student> findByEmail(String email);

    @Query("SELECT new com.mkii.coursemanagementsystem.dto.StudentResponseDTO(s.id, s.fullName, s.email, s.phone, s.address) " +
            "FROM Student s WHERE LOWER(s.fullName) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(s.email) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<StudentResponseDTO> searchByKeyword(@Param("keyword") String keyword);
}
