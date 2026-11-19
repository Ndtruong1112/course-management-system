package com.mkii.coursemanagementsystem.common.converter;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import com.mkii.coursemanagementsystem.util.AESUtil;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mockStatic;

public class AesEncryptConverterTest {

    private final AesEncryptConverter converter = new AesEncryptConverter();

    @Test
    @DisplayName("convertToDatabaseColumn encrypts non-empty string and decrypts back accurately")
    void testEncryptAndDecryptCycle() {
        String originalPhone = "0987654321";
        String encrypted = converter.convertToDatabaseColumn(originalPhone);

        assertNotNull(encrypted);
        assertNotEquals(originalPhone, encrypted);

        String decrypted = converter.convertToEntityAttribute(encrypted);
        assertEquals(originalPhone, decrypted);
    }

    @Test
    @DisplayName("Handles null and blank strings gracefully")
    void testNullAndBlankHandling() {
        assertNull(converter.convertToDatabaseColumn(null));
        assertEquals("", converter.convertToDatabaseColumn(""));
        assertEquals("   ", converter.convertToDatabaseColumn("   "));

        assertNull(converter.convertToEntityAttribute(null));
        assertEquals("", converter.convertToEntityAttribute(""));
        assertEquals("   ", converter.convertToEntityAttribute("   "));
    }

    @Test
    @DisplayName("convertToEntityAttribute falls back to raw data if not encrypted or malformed")
    void testFallbackForUnencryptedData() {
        String plainLegacyAddress = "123 Cau Giay, Hanoi";
        String result = converter.convertToEntityAttribute(plainLegacyAddress);
        assertEquals(plainLegacyAddress, result);
    }

    @Test
    void encryptionFailureDoesNotReturnPlaintext() {
        try (MockedStatic<AESUtil> aes = mockStatic(AESUtil.class)) {
            aes.when(() -> AESUtil.encryptStringWithIv(any(), any()))
                    .thenThrow(new IllegalStateException("encryption unavailable"));
            assertThrows(IllegalStateException.class, () -> converter.convertToDatabaseColumn("sensitive"));
        }
    }
}
