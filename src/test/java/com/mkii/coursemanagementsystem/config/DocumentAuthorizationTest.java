package com.mkii.coursemanagementsystem.config;

import com.mkii.coursemanagementsystem.security.jwt.JwtAccessDeniedHandler;
import com.mkii.coursemanagementsystem.security.jwt.JwtAuthenticationEntryPoint;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import com.mkii.coursemanagementsystem.security.service.UserDetailsServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

import static org.mockito.Mockito.mock;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(SpringExtension.class)
@WebAppConfiguration
@ContextConfiguration(classes = DocumentAuthorizationTest.TestConfiguration.class)
class DocumentAuthorizationTest {
    @Autowired WebApplicationContext context;
    MockMvc mvc;

    @BeforeEach
    void setUp() {
        mvc = MockMvcBuilders.webAppContextSetup(context).apply(SecurityMockMvcConfigurers.springSecurity()).build();
    }

    @Test
    void anonymousAndOrdinaryUsersCannotAccessDocuments() throws Exception {
        mvc.perform(get("/api/documents/list")).andExpect(status().isUnauthorized());
        mvc.perform(get("/api/documents/list").with(user("user").roles("USER"))).andExpect(status().isForbidden());
        mvc.perform(post("/api/documents/upload").with(user("user").roles("USER"))).andExpect(status().isForbidden());
        mvc.perform(post("/api/documents/delete").with(user("user").roles("USER"))).andExpect(status().isForbidden());
    }

    @Test
    void staffCanReadAndUploadButOnlyAdminCanDelete() throws Exception {
        mvc.perform(get("/api/documents/list").with(user("teacher").roles("TEACHER"))).andExpect(status().isOk());
        mvc.perform(post("/api/documents/upload").with(user("teacher").roles("TEACHER"))).andExpect(status().isOk());
        mvc.perform(post("/api/documents/delete").with(user("teacher").roles("TEACHER"))).andExpect(status().isForbidden());
        mvc.perform(delete("/api/documents/1").with(user("teacher").roles("TEACHER"))).andExpect(status().isForbidden());
        mvc.perform(post("/api/documents/delete").with(user("admin").roles("ADMIN"))).andExpect(status().isOk());
        mvc.perform(delete("/api/documents/1").with(user("admin").roles("ADMIN"))).andExpect(status().isOk());
    }

    @Test
    void studentAndEnrollmentReadsRequireStaffRole() throws Exception {
        for (String path : new String[]{"/api/students", "/api/students/list", "/api/students/1", "/api/enrollments", "/api/enrollments/list", "/api/enrollments/student/1"}) {
            mvc.perform(get(path)).andExpect(status().isUnauthorized());
            mvc.perform(get(path).with(user("ordinary").roles("USER"))).andExpect(status().isForbidden());
            mvc.perform(get(path).with(user("teacher").roles("TEACHER"))).andExpect(status().isOk());
            mvc.perform(get(path).with(user("admin").roles("ADMIN"))).andExpect(status().isOk());
            mvc.perform(get(path).with(user("lecturer").roles("LECTURER"))).andExpect(status().isOk());
            mvc.perform(head(path).with(user("ordinary").roles("USER"))).andExpect(status().isForbidden());
        }
    }

    @Configuration
    @EnableWebMvc
    @Import(SecurityConfig.class)
    static class TestConfiguration {
        @Bean UserDetailsServiceImpl userDetailsService() { return mock(UserDetailsServiceImpl.class); }
        @Bean JwtTokenProvider jwtTokenProvider() { return mock(JwtTokenProvider.class); }
        @Bean JwtAuthenticationEntryPoint entryPoint() { return new JwtAuthenticationEntryPoint(); }
        @Bean JwtAccessDeniedHandler deniedHandler() { return new JwtAccessDeniedHandler(); }
        @Bean TestController testController() { return new TestController(); }
    }

    @RestController
    static class TestController {
        @RequestMapping({"/api/documents/**", "/api/students/**", "/api/enrollments/**"})
        String handle() { return "ok"; }
    }
}
