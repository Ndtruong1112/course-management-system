package com.mkii.coursemanagementsystem;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import javax.sql.DataSource;
import jakarta.persistence.EntityManager;
import org.springframework.transaction.annotation.Transactional;
import com.mkii.coursemanagementsystem.dao.IEnrollmentDao;
import com.mkii.coursemanagementsystem.service.CourseService;
import com.mkii.coursemanagementsystem.service.StudentService;
import com.mkii.coursemanagementsystem.entity.Student;
import com.mkii.coursemanagementsystem.entity.Course;
import com.mkii.coursemanagementsystem.entity.Enrollment;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(properties = {
        "spring.datasource.url=jdbc:h2:mem:cms_context_test;MODE=MySQL;DB_CLOSE_DELAY=-1",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "cms.demo-data.enabled=false"
})
class CourseManagementSystemApplicationTests {

    @Autowired DataSource dataSource;
    @Autowired EntityManager entityManager;
    @Autowired IEnrollmentDao enrollmentDao;
    @Autowired CourseService courseService;
    @Autowired StudentService studentService;

    @Test
    void integrationTestsUseIsolatedInMemoryDatabase() throws Exception {
        try (var connection = dataSource.getConnection()) {
            assertTrue(connection.getMetaData().getURL().startsWith("jdbc:h2:mem:"));
        }
    }

    @Test
    @Transactional
    void enrollmentKeywordSearchIsBoundedAndCountsAllMatches() {
        Student student = Student.builder().fullName("Test Learner").email("isolation@example.test").build();
        entityManager.persist(student);
        for (int i = 0; i < 3; i++) {
            Course course = Course.builder().title("Search Target " + i).build();
            entityManager.persist(course);
            entityManager.persist(Enrollment.builder().student(student).course(course).build());
        }
        entityManager.flush();
        var first = enrollmentDao.searchByKeywordPaged("Search Target", 0, 2);
        var second = enrollmentDao.searchByKeywordPaged("Search Target", 1, 2);
        assertEquals(3, first.getTotalElements());
        assertEquals(2, first.getContent().size());
        assertEquals(1, second.getContent().size());
        assertEquals(0, enrollmentDao.searchByKeywordPaged("not present", 0, 2).getTotalElements());
    }

    @Test
    @Transactional
    void courseAndStudentSearchRemainBoundedAndAccurate() {
        for (int i = 0; i < 3; i++) {
            entityManager.persist(Course.builder().title("RAM course " + i).price(100.0 + i).build());
            entityManager.persist(Student.builder().fullName("Memory student " + i).email("ram" + i + "@example.test").build());
        }
        entityManager.flush();
        var courses = courseService.browse("RAM course", 101.0, 102.0, 0, 1);
        assertEquals(2, courses.getTotalElements());
        assertEquals(1, courses.getContent().size());
        var students = studentService.searchPaged("ram", 0, 2);
        assertEquals(3, students.getTotalElements());
        assertEquals(2, students.getContent().size());
        assertEquals(1, studentService.searchPaged("ram", 1, 2).getContent().size());
    }

    @Test
    void contextLoads() {
    }

}
