package com.mkii.coursemanagementsystem.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

public class DateTimeUtilTest {

    @Test
    @DisplayName("format and parse LocalDateTime")
    void testFormatAndParse() {
        LocalDateTime now = LocalDateTime.of(2026, 10, 17, 10, 30, 0);

        String formatted = DateTimeUtil.format(now, DateTimeUtil.DEFAULT_DATETIME_PATTERN);
        assertEquals("2026-10-17 10:30:00", formatted);

        String defaultFormatted = DateTimeUtil.format(now, null);
        assertEquals("2026-10-17 10:30:00", defaultFormatted);

        assertEquals("", DateTimeUtil.format(null, null));

        LocalDateTime parsed = DateTimeUtil.parse("2026-10-17 10:30:00", DateTimeUtil.DEFAULT_DATETIME_PATTERN);
        assertNotNull(parsed);
        assertEquals(now, parsed);

        LocalDateTime defaultParsed = DateTimeUtil.parse("2026-10-17 10:30:00", null);
        assertNotNull(defaultParsed);
        assertEquals(now, defaultParsed);

        assertNull(DateTimeUtil.parse(null, null));
        assertNull(DateTimeUtil.parse("  ", null));
    }

    @Test
    @DisplayName("toEpochMillis and fromEpochMillis conversions")
    void testEpochConversions() {
        LocalDateTime now = LocalDateTime.of(2026, 10, 17, 12, 0, 0);

        long millis = DateTimeUtil.toEpochMillis(now);
        assertTrue(millis > 0);

        assertEquals(0L, DateTimeUtil.toEpochMillis(null));

        LocalDateTime reconstructed = DateTimeUtil.fromEpochMillis(millis);
        assertNotNull(reconstructed);
        assertEquals(now.getYear(), reconstructed.getYear());
        assertEquals(now.getMonth(), reconstructed.getMonth());
        assertEquals(now.getDayOfMonth(), reconstructed.getDayOfMonth());
    }

    @Test
    @DisplayName("DateTimeUtil private constructor throws UnsupportedOperationException")
    void testPrivateConstructor() throws Exception {
        Constructor<DateTimeUtil> constructor = DateTimeUtil.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class, constructor::newInstance);
        assertInstanceOf(UnsupportedOperationException.class, ex.getCause());
    }
}
