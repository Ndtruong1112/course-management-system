package com.mkii.coursemanagementsystem.config;

import com.mkii.coursemanagementsystem.dao.*;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;

class DataInitializerConfigurationTest {
    private final ApplicationContextRunner runner = new ApplicationContextRunner()
            .withUserConfiguration(DataInitializer.class)
            .withBean(IDepartmentDao.class, () -> mock(IDepartmentDao.class))
            .withBean(IUserDao.class, () -> mock(IUserDao.class))
            .withBean(ICourseDao.class, () -> mock(ICourseDao.class))
            .withBean(IStudentDao.class, () -> mock(IStudentDao.class))
            .withBean(IEnrollmentDao.class, () -> mock(IEnrollmentDao.class))
            .withBean(PasswordEncoder.class, () -> mock(PasswordEncoder.class));

    @Test
    void demoDataIsDisabledByDefault() {
        runner.run(context -> assertThat(context).doesNotHaveBean(DataInitializer.class));
    }

    @Test
    void demoDataMustBeExplicitlyEnabledAndCannotRunInProduction() {
        runner.withPropertyValues("cms.demo-data.enabled=true")
                .run(context -> assertThat(context).hasSingleBean(DataInitializer.class));
        runner.withPropertyValues("cms.demo-data.enabled=true", "spring.profiles.active=prod")
                .run(context -> assertThat(context).doesNotHaveBean(DataInitializer.class));
    }
}
