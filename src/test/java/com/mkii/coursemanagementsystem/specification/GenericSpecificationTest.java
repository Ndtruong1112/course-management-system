package com.mkii.coursemanagementsystem.specification;

import com.mkii.coursemanagementsystem.entity.Course;
import org.junit.jupiter.api.Test;
import org.springframework.data.jpa.domain.Specification;

import static org.junit.jupiter.api.Assertions.*;

class GenericSpecificationTest {

    @Test
    void testSearchQueryParsingPrecedence() {
        GenericSpecificationsBuilder<Course> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery("price>=100,price<=500,duration>30,title:Java,price!=999");

        Specification<Course> spec = builder.build();
        assertNotNull(spec, "Specification should not be null after parsing query");
    }

    @Test
    void testEmptyQueryReturnsNull() {
        GenericSpecificationsBuilder<Course> builder = new GenericSpecificationsBuilder<>();
        builder.withSearchQuery("");

        Specification<Course> spec = builder.build();
        assertNull(spec, "Specification should be null for empty query");
    }
}
