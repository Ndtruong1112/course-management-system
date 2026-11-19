package com.mkii.coursemanagementsystem.service;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.dao.IDocumentDao;
import com.mkii.coursemanagementsystem.entity.Document;
import com.mkii.coursemanagementsystem.service.impl.DocumentServiceImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DocumentServiceTest {

    @Mock
    private IDocumentDao documentDao;

    @Mock
    private MinioStorageService minioStorageService;

    @InjectMocks
    private DocumentServiceImpl documentService;

    @Test
    void downloadStreamsAndClosesInputWithoutBufferingEntireFile() throws Exception {
        class TrackedInput extends ByteArrayInputStream {
            boolean closed;
            TrackedInput(byte[] data) { super(data); }
            @Override public void close() throws IOException { closed = true; super.close(); }
        }
        var input = new TrackedInput("file-content".getBytes(StandardCharsets.UTF_8));
        when(minioStorageService.openDownload("folder/test.pdf")).thenReturn(input);
        var response = documentService.download("folder/test.pdf");
        verify(minioStorageService, never()).openDownload(anyString());
        var output = new ByteArrayOutputStream();
        response.getBody().writeTo(output);
        assertEquals("file-content", output.toString(StandardCharsets.UTF_8));
        assertTrue(input.closed);
        verify(minioStorageService).openDownload("folder/test.pdf");
    }

    @Test
    void downloadReadsLargeObjectInBoundedChunks() throws Exception {
        class GeneratedInput extends InputStream {
            long remaining = 32L * 1024 * 1024;
            int largestRead;
            boolean closed;
            @Override public int read() { if (remaining == 0) return -1; remaining--; return 0; }
            @Override public int read(byte[] bytes, int offset, int length) {
                if (remaining == 0) return -1;
                largestRead = Math.max(largestRead, length);
                int count = (int) Math.min(length, remaining);
                remaining -= count;
                return count;
            }
            @Override public void close() { closed = true; }
        }
        var input = new GeneratedInput();
        when(minioStorageService.openDownload("large.bin")).thenReturn(input);
        var response = documentService.download("large.bin");
        response.getBody().writeTo(OutputStream.nullOutputStream());
        assertEquals(0, input.remaining);
        assertTrue(input.largestRead <= 65536, "Must not allocate a buffer proportional to file size");
        assertTrue(input.closed);
    }

    @Test
    void testCreateWithValidFileExtension() {
        MockMultipartFile file = new MockMultipartFile(
                "files",
                "test.pdf",
                "application/pdf",
                "Hello PDF".getBytes()
        );

        when(documentDao.save(any(Document.class))).thenAnswer(invocation -> {
            Document doc = invocation.getArgument(0);
            doc.setId("uuid-123");
            return doc;
        });

        List<Document> result = documentService.create(List.of(file), "APP_COURSE_101");
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("test.pdf", result.get(0).getName());
        assertEquals("APP_COURSE_101", result.get(0).getAppId());
        verify(minioStorageService, times(1)).upload(anyString(), any(), any(), anyLong());
    }

    @Test
    void testCreateWithInvalidFileExtensionThrowsException() {
        MockMultipartFile invalidFile = new MockMultipartFile(
                "files",
                "virus.exe",
                "application/octet-stream",
                "bad bytes".getBytes()
        );

        assertThrows(BadRequestException.class, () ->
                documentService.create(List.of(invalidFile), "APP_COURSE_101")
        );
        verify(minioStorageService, never()).upload(anyString(), any(), any(), anyLong());
    }

    @Test
    void testSoftDeleteDocument() {
        Document mockDoc = Document.builder()
                .id("doc-001")
                .name("sample.docx")
                .appId("APP_01")
                .deleted(false)
                .active(true)
                .build();

        when(documentDao.findByPk("doc-001")).thenReturn(mockDoc);

        String response = documentService.delete(Map.of("id", "doc-001"));
        assertNotNull(response);
        assertTrue(mockDoc.getDeleted());
        assertFalse(mockDoc.getActive());
        verify(documentDao, times(1)).update(mockDoc);
    }

    @Test
    void testCreateWithVersionIncrementWhenFileAlreadyExists() {
        MockMultipartFile file = new MockMultipartFile(
                "files",
                "syllabus.pdf",
                "application/pdf",
                "Updated PDF".getBytes()
        );

        Document existingDoc = Document.builder()
                .id("doc-v1")
                .name("syllabus.pdf")
                .appId("APP_COURSE_101")
                .version(1.0)
                .active(true)
                .deleted(false)
                .build();

        when(documentDao.getDocumentName("syllabus.pdf", "APP_COURSE_101")).thenReturn(existingDoc);
        when(documentDao.save(any(Document.class))).thenAnswer(invocation -> {
            Document doc = invocation.getArgument(0);
            doc.setId("doc-v2");
            return doc;
        });

        List<Document> result = documentService.create(List.of(file), "APP_COURSE_101");
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(2.0, result.get(0).getVersion());
        assertFalse(existingDoc.getActive());
        verify(documentDao, times(1)).update(existingDoc);
        verify(documentDao, times(1)).save(any(Document.class));
    }

    @Test
    void testGetDocPaginationAndSorting() {
        Document doc1 = Document.builder().id("1").name("file1.pdf").build();
        when(documentDao.getDoc("file", 0, 10, "creationTime", "desc", "APP_01"))
                .thenReturn(List.of(doc1));

        List<Document> result = documentService.getDoc("file", 0, 10, "creationTime", "desc", "APP_01");
        assertEquals(1, result.size());
        verify(documentDao, times(1)).getDoc("file", 0, 10, "creationTime", "desc", "APP_01");
    }

    @Test
    void testGetDocCount() {
        when(documentDao.getDocCount("file", "APP_01")).thenReturn(5);

        Integer count = documentService.getDocCount("file", "APP_01");
        assertEquals(5, count);
        verify(documentDao, times(1)).getDocCount("file", "APP_01");
    }
}
