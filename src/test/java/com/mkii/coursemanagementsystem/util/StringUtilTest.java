package com.mkii.coursemanagementsystem.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

import static org.junit.jupiter.api.Assertions.*;

public class StringUtilTest {

    @Test
    @DisplayName("isEmpty and isNotEmpty tests")
    void testEmptyChecks() {
        assertTrue(StringUtil.isEmpty(null));
        assertTrue(StringUtil.isEmpty(""));
        assertFalse(StringUtil.isEmpty("a"));

        assertFalse(StringUtil.isNotEmpty(null));
        assertFalse(StringUtil.isNotEmpty(""));
        assertTrue(StringUtil.isNotEmpty("a"));
    }

    @Test
    @DisplayName("isBlank and isNotBlank tests")
    void testBlankChecks() {
        assertTrue(StringUtil.isBlank(null));
        assertTrue(StringUtil.isBlank("   "));
        assertFalse(StringUtil.isBlank(" hello "));

        assertFalse(StringUtil.isNotBlank(null));
        assertFalse(StringUtil.isNotBlank("   "));
        assertTrue(StringUtil.isNotBlank(" hello "));
    }

    @Test
    @DisplayName("maskSensitive masks middle characters")
    void testMaskSensitive() {
        assertNull(StringUtil.maskSensitive(null, 2, 2));
        assertEquals("****", StringUtil.maskSensitive("pass", 2, 2));
        assertEquals("se**********78", StringUtil.maskSensitive("secret12345678", 2, 2));
    }

    @Test
    @DisplayName("maskEmail masks local part properly")
    void testMaskEmail() {
        assertNull(StringUtil.maskEmail(null));
        assertEquals("s*****t@example.com", StringUtil.maskEmail("student@example.com"));
        assertEquals("**@domain.com", StringUtil.maskEmail("ab@domain.com"));
        assertEquals("n********l", StringUtil.maskEmail("notanemail"));
    }

    @Test
    @DisplayName("toSlug converts Vietnamese text with diacritics into URL slug")
    void testToSlug() {
        assertEquals("", StringUtil.toSlug(null));
        assertEquals("", StringUtil.toSlug("   "));
        assertEquals("lap-trinh-java-co-ban", StringUtil.toSlug("Lập trình Java Cơ Bản"));
        assertEquals("khoa-hoc-spring-boot-2026", StringUtil.toSlug("Khóa học Spring Boot 2026!"));
        assertEquals("dai-hoc-quoc-gia", StringUtil.toSlug("Đại học Quốc gia"));
    }

    @Test
    @DisplayName("StringUtil private constructor throws UnsupportedOperationException")
    void testPrivateConstructor() throws Exception {
        Constructor<StringUtil> constructor = StringUtil.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class, constructor::newInstance);
        assertInstanceOf(UnsupportedOperationException.class, ex.getCause());
    }
}
