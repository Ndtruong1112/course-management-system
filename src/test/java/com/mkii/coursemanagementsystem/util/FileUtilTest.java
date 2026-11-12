package com.mkii.coursemanagementsystem.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

import static org.junit.jupiter.api.Assertions.*;

public class FileUtilTest {

    @Test
    @DisplayName("checkFileNameSpecialChar identifies valid and invalid file names")
    void testCheckFileNameSpecialChar() {
        assertTrue(FileUtil.checkFileNameSpecialChar("valid_document-2026.pdf"));
        assertTrue(FileUtil.checkFileNameSpecialChar("report.final.docx"));
        assertFalse(FileUtil.checkFileNameSpecialChar("invalid/file.pdf"));
        assertFalse(FileUtil.checkFileNameSpecialChar("file$name.pdf"));
        assertFalse(FileUtil.checkFileNameSpecialChar("bad*name?.txt"));
        assertFalse(FileUtil.checkFileNameSpecialChar(null));
        assertFalse(FileUtil.checkFileNameSpecialChar("   "));
    }

    @Test
    @DisplayName("getFileExtension extracts lowercase extension safely")
    void testGetFileExtension() {
        assertEquals("pdf", FileUtil.getFileExtension("document.PDF"));
        assertEquals("docx", FileUtil.getFileExtension("archive.v1.DOCX"));
        assertEquals("", FileUtil.getFileExtension("filename_without_extension"));
        assertEquals("", FileUtil.getFileExtension(null));
    }

    @Test
    @DisplayName("sanitizeFileName cleans path traversal and unsafe characters")
    void testSanitizeFileName() {
        assertEquals("test_file.pdf", FileUtil.sanitizeFileName("test_file.pdf"));
        assertEquals("_etc_passwd", FileUtil.sanitizeFileName("/etc/passwd"));
        assertEquals("._secret.txt", FileUtil.sanitizeFileName("../secret.txt"));
        assertEquals("", FileUtil.sanitizeFileName(null));
    }

    @Test
    @DisplayName("formatFileSize converts bytes to readable string")
    void testFormatFileSize() {
        assertEquals("0 B", FileUtil.formatFileSize(0));
        assertEquals("0 B", FileUtil.formatFileSize(-100));
        assertEquals("500 B", FileUtil.formatFileSize(500));
        assertEquals("1 KB", FileUtil.formatFileSize(1024));
        assertEquals("1.5 MB", FileUtil.formatFileSize((long) (1.5 * 1024 * 1024)));
        assertEquals("2 GB", FileUtil.formatFileSize(2L * 1024 * 1024 * 1024));
    }

    @Test
    @DisplayName("isValidFileSize validates constraints")
    void testIsValidFileSize() {
        assertTrue(FileUtil.isValidFileSize(1024, 2048));
        assertFalse(FileUtil.isValidFileSize(4096, 2048));
        assertFalse(FileUtil.isValidFileSize(0, 2048));
        assertFalse(FileUtil.isValidFileSize(-1, 2048));
    }

    @Test
    @DisplayName("FileUtil private constructor throws UnsupportedOperationException")
    void testPrivateConstructor() throws Exception {
        Constructor<FileUtil> constructor = FileUtil.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class, constructor::newInstance);
        assertInstanceOf(UnsupportedOperationException.class, ex.getCause());
    }
}
