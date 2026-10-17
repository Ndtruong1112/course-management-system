package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "courses", indexes = {
        @Index(name = "idx_course_title", columnList = "title"),
        @Index(name = "idx_course_price", columnList = "price")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    private Integer duration;

    private Double price;
}