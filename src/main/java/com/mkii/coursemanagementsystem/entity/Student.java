package com.mkii.coursemanagementsystem.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "students", indexes = {
        @Index(name = "idx_student_email", columnList = "email"),
        @Index(name = "idx_student_fullname", columnList = "fullName")
})
@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id;

    @Column(nullable = false, length = 150)
    private String fullName;

    @Column(nullable = false, unique = true, length = 150)
    private String email;

    @Column(length = 20)
    private String phone;

    @Column(length = 255)
    private String address;
}
