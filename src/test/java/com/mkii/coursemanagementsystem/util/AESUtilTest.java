package com.mkii.coursemanagementsystem.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import javax.crypto.SealedObject;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.IvParameterSpec;
import java.io.File;
import java.io.Serializable;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

public class AESUtilTest {

    @TempDir
    Path tempDir;

    static class SampleData implements Serializable {
        private static final long serialVersionUID = 1L;
        String name;
        int age;

        SampleData(String name, int age) {
            this.name = name;
            this.age = age;
        }
    }

    @Test
    @DisplayName("Generate AES key with 128, 192, and 256 bits")
    void testGenerateKey() throws Exception {
        SecretKey key128 = AESUtil.generateKey(128);
        assertNotNull(key128);
        assertEquals("AES", key128.getAlgorithm());

        SecretKey key256 = AESUtil.generateKey(256);
        assertNotNull(key256);
        assertEquals("AES", key256.getAlgorithm());
    }

    @Test
    @DisplayName("Derive key from password and salt using PBKDF2")
    void testGetKeyFromPassword() throws Exception {
        SecretKey key = AESUtil.getKeyFromPassword("MyStrongPassword@123", "salt_value_123");
        assertNotNull(key);
        assertEquals("AES", key.getAlgorithm());

        assertThrows(IllegalArgumentException.class, () -> AESUtil.getKeyFromPassword(null, "salt"));
        assertThrows(IllegalArgumentException.class, () -> AESUtil.getKeyFromPassword("pass", null));
    }

    @Test
    @DisplayName("Generate CBC and GCM Initialization Vectors")
    void testGenerateIv() {
        IvParameterSpec iv = AESUtil.generateIv();
        assertNotNull(iv);
        assertEquals(16, iv.getIV().length);

        GCMParameterSpec gcmIv = AESUtil.generateGcmIv();
        assertNotNull(gcmIv);
        assertEquals(12, gcmIv.getIV().length);
        assertEquals(128, gcmIv.getTLen());
    }

    @Test
    @DisplayName("Encrypt and decrypt string using AES/CBC/PKCS5Padding")
    void testEncryptDecrypt_CBC() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        IvParameterSpec iv = AESUtil.generateIv();
        String plain = "Hello, Course Management System AES!";

        String cipher = AESUtil.encrypt(AESUtil.DEFAULT_ALGORITHM, plain, key, iv);
        assertNotNull(cipher);
        assertNotEquals(plain, cipher);

        String decrypted = AESUtil.decrypt(AESUtil.DEFAULT_ALGORITHM, cipher, key, iv);
        assertEquals(plain, decrypted);

        assertNull(AESUtil.encrypt(AESUtil.DEFAULT_ALGORITHM, null, key, iv));
        assertNull(AESUtil.decrypt(AESUtil.DEFAULT_ALGORITHM, null, key, iv));
    }

    @Test
    @DisplayName("Encrypt and decrypt string using AES/GCM/NoPadding")
    void testEncryptDecrypt_GCM() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        GCMParameterSpec iv = AESUtil.generateGcmIv();
        String plain = "Sensitive student credential payload";

        String cipher = AESUtil.encryptGcm(plain, key, iv);
        assertNotNull(cipher);
        assertNotEquals(plain, cipher);

        String decrypted = AESUtil.decryptGcm(cipher, key, iv);
        assertEquals(plain, decrypted);

        assertNull(AESUtil.encryptGcm(null, key, iv));
        assertNull(AESUtil.decryptGcm(null, key, iv));
    }

    @Test
    @DisplayName("Encrypt and decrypt Java Serializable object as SealedObject")
    void testEncryptDecryptObject() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        IvParameterSpec iv = AESUtil.generateIv();
        SampleData data = new SampleData("Baeldung Learner", 25);

        SealedObject sealed = AESUtil.encryptObject(AESUtil.DEFAULT_ALGORITHM, data, key, iv);
        assertNotNull(sealed);

        SampleData unsealed = (SampleData) AESUtil.decryptObject(AESUtil.DEFAULT_ALGORITHM, sealed, key, iv);
        assertNotNull(unsealed);
        assertEquals(data.name, unsealed.name);
        assertEquals(data.age, unsealed.age);
    }

    @Test
    @DisplayName("Encrypt and decrypt file stream using AES")
    void testEncryptDecryptFile() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        IvParameterSpec iv = AESUtil.generateIv();

        File inputFile = tempDir.resolve("original.txt").toFile();
        File encryptedFile = tempDir.resolve("encrypted.enc").toFile();
        File decryptedFile = tempDir.resolve("decrypted.txt").toFile();

        String content = "Confidential syllabus data for year 2026";
        Files.writeString(inputFile.toPath(), content);

        AESUtil.encryptFile(AESUtil.DEFAULT_ALGORITHM, key, iv, inputFile, encryptedFile);
        assertTrue(encryptedFile.exists());
        assertTrue(encryptedFile.length() > 0);

        AESUtil.decryptFile(AESUtil.DEFAULT_ALGORITHM, key, iv, encryptedFile, decryptedFile);
        assertTrue(decryptedFile.exists());
        assertEquals(content, Files.readString(decryptedFile.toPath()));
    }

    @Test
    @DisplayName("Encrypt and decrypt raw byte array with prepended IV")
    void testEncryptDecryptBytesWithIv() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        byte[] original = "Raw byte array payload for MinIO".getBytes(java.nio.charset.StandardCharsets.UTF_8);

        byte[] encrypted = AESUtil.encryptBytesWithIv(original, key);
        assertNotNull(encrypted);
        assertTrue(encrypted.length > original.length);

        byte[] decrypted = AESUtil.decryptBytesWithIv(encrypted, key);
        assertArrayEquals(original, decrypted);

        assertNull(AESUtil.encryptBytesWithIv(null, key));
        assertNull(AESUtil.decryptBytesWithIv(null, key));
        byte[] shortBytes = new byte[5];
        assertSame(shortBytes, AESUtil.decryptBytesWithIv(shortBytes, key));
    }

    @Test
    @DisplayName("Encrypt and decrypt String with prepended IV")
    void testEncryptDecryptStringWithIv() throws Exception {
        SecretKey key = AESUtil.generateKey(128);
        String plain = "Hello Secure World 2026!";

        String cipher = AESUtil.encryptStringWithIv(plain, key);
        assertNotNull(cipher);
        assertNotEquals(plain, cipher);

        String decrypted = AESUtil.decryptStringWithIv(cipher, key);
        assertEquals(plain, decrypted);

        assertNull(AESUtil.encryptStringWithIv(null, key));
        assertNull(AESUtil.decryptStringWithIv(null, key));
    }

    @Test
    @DisplayName("AESUtil private constructor throws UnsupportedOperationException")
    void testPrivateConstructor() throws Exception {
        Constructor<AESUtil> constructor = AESUtil.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class, constructor::newInstance);
        assertInstanceOf(UnsupportedOperationException.class, ex.getCause());
    }
}
