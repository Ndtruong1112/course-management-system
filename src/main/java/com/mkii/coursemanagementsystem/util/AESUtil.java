package com.mkii.coursemanagementsystem.util;

import javax.crypto.*;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Base64;

/**
 * Technical helper utility providing static methods for AES Encryption and Decryption,
 * key generation, password-based key derivation (PBKDF2), initialization vectors (IV),
 * String, File, and SealedObject operations.
 *
 * Implemented based on official Baeldung Java AES Encryption and Decryption standards.
 */
public final class AESUtil {

    public static final String DEFAULT_ALGORITHM = "AES/CBC/PKCS5Padding";
    public static final String GCM_ALGORITHM = "AES/GCM/NoPadding";
    public static final int GCM_TAG_LENGTH = 128;
    public static final int DEFAULT_IV_SIZE = 16;
    public static final int GCM_IV_SIZE = 12;
    public static final int PBKDF2_ITERATIONS = 65536;
    public static final int PBKDF2_KEY_LENGTH = 256;

    private AESUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Generates a random AES SecretKey with the specified bit size (128, 192, 256).
     */
    public static SecretKey generateKey(int n) throws NoSuchAlgorithmException {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(n);
        return keyGenerator.generateKey();
    }

    /**
     * Derives an AES SecretKey from a given password and salt using PBKDF2WithHmacSHA256.
     */
    public static SecretKey getKeyFromPassword(String password, String salt)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        if (password == null || salt == null) {
            throw new IllegalArgumentException("Password and salt cannot be null");
        }
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(StandardCharsets.UTF_8), PBKDF2_ITERATIONS, PBKDF2_KEY_LENGTH);
        return new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
    }

    /**
     * Generates a cryptographically random 16-byte Initialization Vector (IV) for CBC mode.
     */
    public static IvParameterSpec generateIv() {
        byte[] iv = new byte[DEFAULT_IV_SIZE];
        new SecureRandom().nextBytes(iv);
        return new IvParameterSpec(iv);
    }

    /**
     * Generates a cryptographically random 12-byte IV for GCM mode with 128-bit authentication tag.
     */
    public static GCMParameterSpec generateGcmIv() {
        byte[] iv = new byte[GCM_IV_SIZE];
        new SecureRandom().nextBytes(iv);
        return new GCMParameterSpec(GCM_TAG_LENGTH, iv);
    }

    /**
     * Encrypts a plaintext String using AES with IvParameterSpec (e.g. CBC mode) and returns Base64 ciphertext.
     */
    public static String encrypt(String algorithm, String input, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] cipherText = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(cipherText);
    }

    /**
     * Decrypts a Base64 ciphertext String using AES with IvParameterSpec (e.g. CBC mode).
     */
    public static String decrypt(String algorithm, String cipherText, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (cipherText == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText, StandardCharsets.UTF_8);
    }

    /**
     * Encrypts a plaintext String using AES with GCMParameterSpec (e.g. GCM mode) and returns Base64 ciphertext.
     */
    public static String encryptGcm(String input, SecretKey key, GCMParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(GCM_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] cipherText = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(cipherText);
    }

    /**
     * Decrypts a Base64 ciphertext String using AES with GCMParameterSpec (e.g. GCM mode).
     */
    public static String decryptGcm(String cipherText, SecretKey key, GCMParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (cipherText == null) {
            return null;
        }
        Cipher cipher = Cipher.getInstance(GCM_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        byte[] plainText = cipher.doFinal(Base64.getDecoder().decode(cipherText));
        return new String(plainText, StandardCharsets.UTF_8);
    }

    /**
     * Encrypts a Serializable Java Object into a SealedObject using AES.
     */
    public static SealedObject encryptObject(String algorithm, Serializable object, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, IOException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        return new SealedObject(object, cipher);
    }

    /**
     * Decrypts a SealedObject back into its original Serializable Java Object.
     */
    public static Serializable decryptObject(String algorithm, SealedObject sealedObject, SecretKey key, IvParameterSpec iv)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, ClassNotFoundException, BadPaddingException, IllegalBlockSizeException, IOException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        return (Serializable) sealedObject.getObject(cipher);
    }

    /**
     * Encrypts an input File to an output File using AES and stream buffering.
     */
    public static void encryptFile(String algorithm, SecretKey key, IvParameterSpec iv, File inputFile, File outputFile)
            throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        processFile(cipher, inputFile, outputFile);
    }

    /**
     * Decrypts an encrypted File to an output File using AES and stream buffering.
     */
    public static void decryptFile(String algorithm, SecretKey key, IvParameterSpec iv, File inputFile, File outputFile)
            throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance(algorithm != null ? algorithm : DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        processFile(cipher, inputFile, outputFile);
    }

    private static void processFile(Cipher cipher, File inputFile, File outputFile)
            throws IOException, BadPaddingException, IllegalBlockSizeException {
        try (FileInputStream inputStream = new FileInputStream(inputFile);
             FileOutputStream outputStream = new FileOutputStream(outputFile)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                byte[] output = cipher.update(buffer, 0, bytesRead);
                if (output != null) {
                    outputStream.write(output);
                }
            }
            byte[] outputBytes = cipher.doFinal();
            if (outputBytes != null) {
                outputStream.write(outputBytes);
            }
        }
    }

    /**
     * Encrypts a raw byte array by generating a random 16-byte IV, encrypting the bytes,
     * and prepending the IV to the ciphertext [IV (16 bytes) | Encrypted payload].
     */
    public static byte[] encryptBytesWithIv(byte[] input, SecretKey key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null) {
            return null;
        }
        IvParameterSpec iv = generateIv();
        Cipher cipher = Cipher.getInstance(DEFAULT_ALGORITHM);
        cipher.init(Cipher.ENCRYPT_MODE, key, iv);
        byte[] encrypted = cipher.doFinal(input);
        byte[] result = new byte[DEFAULT_IV_SIZE + encrypted.length];
        System.arraycopy(iv.getIV(), 0, result, 0, DEFAULT_IV_SIZE);
        System.arraycopy(encrypted, 0, result, DEFAULT_IV_SIZE, encrypted.length);
        return result;
    }

    /**
     * Decrypts a raw byte array formatted as [IV (16 bytes) | Encrypted payload].
     */
    public static byte[] decryptBytesWithIv(byte[] input, SecretKey key)
            throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidAlgorithmParameterException,
            InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        if (input == null || input.length <= DEFAULT_IV_SIZE) {
            return input;
        }
        byte[] ivBytes = new byte[DEFAULT_IV_SIZE];
        System.arraycopy(input, 0, ivBytes, 0, DEFAULT_IV_SIZE);
        IvParameterSpec iv = new IvParameterSpec(ivBytes);

        Cipher cipher = Cipher.getInstance(DEFAULT_ALGORITHM);
        cipher.init(Cipher.DECRYPT_MODE, key, iv);
        return cipher.doFinal(input, DEFAULT_IV_SIZE, input.length - DEFAULT_IV_SIZE);
    }

    /**
     * Encrypts plaintext string with prepended IV and returns a Base64 encoded string.
     */
    public static String encryptStringWithIv(String plainText, SecretKey key) throws Exception {
        if (plainText == null) {
            return null;
        }
        byte[] encrypted = encryptBytesWithIv(plainText.getBytes(StandardCharsets.UTF_8), key);
        return Base64.getEncoder().encodeToString(encrypted);
    }

    /**
     * Decrypts a Base64 string that has prepended IV.
     */
    public static String decryptStringWithIv(String cipherText, SecretKey key) throws Exception {
        if (cipherText == null) {
            return null;
        }
        byte[] decoded = Base64.getDecoder().decode(cipherText);
        byte[] decrypted = decryptBytesWithIv(decoded, key);
        return new String(decrypted, StandardCharsets.UTF_8);
    }
}
