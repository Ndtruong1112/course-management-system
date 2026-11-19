package com.mkii.coursemanagementsystem.rest;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mkii.coursemanagementsystem.common.ApiConstants;
import com.mkii.coursemanagementsystem.dto.DecryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.DecryptResponseDTO;
import com.mkii.coursemanagementsystem.dto.EncryptRequestDTO;
import com.mkii.coursemanagementsystem.dto.EncryptResponseDTO;
import com.mkii.coursemanagementsystem.service.MinioStorageService;
import com.mkii.coursemanagementsystem.service.SecurityService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.asyncDispatch;
import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {
        "spring.datasource.url=jdbc:h2:mem:cms_security_test;MODE=MySQL;DB_CLOSE_DELAY=-1",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "cms.demo-data.enabled=false"
})
@AutoConfigureMockMvc
public class SecurityRestImplTest {

    @Autowired
    private MockMvc mockMvc;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @MockitoBean
    private SecurityService securityService;

    @MockitoBean
    private MinioStorageService minioStorageService;

    @Test
    @DisplayName("Dashboard serves bounded enrollment loading")
    void dashboardContainsPagedEnrollmentLoader() throws Exception {
        mockMvc.perform(get("/index.html"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("/api/enrollments/paged?page=")))
                .andExpect(content().string(containsString("enrollPageInfo")));
    }

    @Test
    @DisplayName("Paged enrollment search is available to staff only")
    void pagedEnrollmentSearchRespectsAuthorization() throws Exception {
        mockMvc.perform(get("/api/enrollments/search-paged").param("keyword", "example")
                        .with(user("teacher").roles("TEACHER")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray())
                .andExpect(jsonPath("$.size").value(20));
        mockMvc.perform(get("/api/enrollments/search-paged").param("keyword", "example")
                        .with(user("ordinary").roles("USER")))
                .andExpect(status().isForbidden());
        mockMvc.perform(get("/api/enrollments/search-paged").param("keyword", "example"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Paged course and student search keep authorization rules")
    void boundedSearchAuthorization() throws Exception {
        mockMvc.perform(get("/api/courses/browse").param("keyword", "course"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.content").isArray());
        mockMvc.perform(get("/api/students/search-paged").param("keyword", "student")
                        .with(user("teacher").roles("TEACHER")))
                .andExpect(status().isOk()).andExpect(jsonPath("$.content").isArray());
        mockMvc.perform(get("/api/students/search-paged").param("keyword", "student")
                        .with(user("ordinary").roles("USER")))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("Staff download streams bytes and preserves response headers")
    void staffCanStreamDocument() throws Exception {
        when(minioStorageService.openDownload("folder/file.pdf"))
                .thenReturn(new ByteArrayInputStream("file-content".getBytes(StandardCharsets.UTF_8)));
        MvcResult result = mockMvc.perform(get("/api/documents/download")
                        .param("filePath", "folder/file.pdf").with(user("teacher").roles("TEACHER")))
                .andExpect(request().asyncStarted())
                .andReturn();
        mockMvc.perform(asyncDispatch(result))
                .andExpect(status().isOk())
                .andExpect(header().string("Content-Disposition", containsString("file.pdf")))
                .andExpect(content().string("file-content"));
        mockMvc.perform(get("/api/documents/download")
                        .param("filePath", "folder/file.pdf").with(user("ordinary").roles("USER")))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("Admin can encrypt payload - 200 OK")
    void testEncrypt_Admin_Success() throws Exception {
        EncryptRequestDTO request = EncryptRequestDTO.builder().data("SecretMessage").build();
        EncryptResponseDTO response = EncryptResponseDTO.builder()
                .encryptedData("EncryptedBase64WithIv")
                .algorithm("AES/CBC/PKCS5Padding")
                .build();

        when(securityService.encrypt(any(EncryptRequestDTO.class))).thenReturn(response);

        mockMvc.perform(post(ApiConstants.BASE_SECURITY_URL + "/encrypt")
                        .with(user("admin").roles("ADMIN"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.encryptedData").value("EncryptedBase64WithIv"))
                .andExpect(jsonPath("$.algorithm").value("AES/CBC/PKCS5Padding"));
    }

    @Test
    @DisplayName("Teacher can encrypt payload - 200 OK")
    void testEncrypt_Teacher_Success() throws Exception {
        EncryptRequestDTO request = EncryptRequestDTO.builder().data("SecretMessage").build();
        EncryptResponseDTO response = EncryptResponseDTO.builder()
                .encryptedData("EncryptedBase64WithIv")
                .algorithm("AES/CBC/PKCS5Padding")
                .build();

        when(securityService.encrypt(any(EncryptRequestDTO.class))).thenReturn(response);

        mockMvc.perform(post(ApiConstants.BASE_SECURITY_URL + "/encrypt")
                        .with(user("gv_nam").roles("TEACHER"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.encryptedData").value("EncryptedBase64WithIv"))
                .andExpect(jsonPath("$.algorithm").value("AES/CBC/PKCS5Padding"));
    }

    @Test
    @DisplayName("Lecturer can decrypt payload - 200 OK")
    void testDecrypt_Lecturer_Success() throws Exception {
        DecryptRequestDTO request = DecryptRequestDTO.builder().encryptedData("EncryptedBase64WithIv").build();
        DecryptResponseDTO response = DecryptResponseDTO.builder().decryptedData("SecretMessage").build();

        when(securityService.decrypt(any(DecryptRequestDTO.class))).thenReturn(response);

        mockMvc.perform(post(ApiConstants.BASE_SECURITY_URL + "/decrypt")
                        .with(user("lecturer").roles("LECTURER"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.decryptedData").value("SecretMessage"));
    }

    @Test
    @DisplayName("Student is forbidden from encrypt endpoint - 403 Forbidden")
    void testEncrypt_Student_Forbidden() throws Exception {
        EncryptRequestDTO request = EncryptRequestDTO.builder().data("SecretMessage").build();

        mockMvc.perform(post(ApiConstants.BASE_SECURITY_URL + "/encrypt")
                        .with(user("student").roles("STUDENT"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("Unauthenticated request without required token is unauthorized - 401 Unauthorized")
    void testEncrypt_Unauthenticated_Forbidden() throws Exception {
        EncryptRequestDTO request = EncryptRequestDTO.builder().data("SecretMessage").build();

        mockMvc.perform(post(ApiConstants.BASE_SECURITY_URL + "/encrypt")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isUnauthorized());
    }
}
