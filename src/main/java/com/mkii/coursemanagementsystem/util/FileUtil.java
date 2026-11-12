package com.mkii.coursemanagementsystem.util;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;
import java.util.regex.Pattern;

/**
 * Technical helper utility providing static methods for file name validation,
 * extension extraction, sanitization against path traversal, and byte size formatting.
 * Contains purely technical methods without any business logic.
 */
public final class FileUtil {

    private static final Pattern SAFE_FILENAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_.-]+$");
    private static final String[] SIZE_UNITS = new String[]{"B", "KB", "MB", "GB", "TB"};

    private FileUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    /**
     * Checks if a file name contains only safe characters (alphanumeric, dot, underscore, dash).
     * Returns true if safe, false if contains invalid/special characters.
     */
    public static boolean checkFileNameSpecialChar(String fileName) {
        if (fileName == null || fileName.trim().isEmpty()) {
            return false;
        }
        return SAFE_FILENAME_PATTERN.matcher(fileName.trim()).matches();
    }

    /**
     * Extracts the extension of a file name in lowercase (e.g. "document.PDF" -> "pdf").
     * Returns empty string if no extension is present.
     */
    public static String getFileExtension(String fileName) {
        if (fileName == null || fileName.lastIndexOf('.') == -1) {
            return "";
        }
        return fileName.substring(fileName.lastIndexOf('.') + 1).trim().toLowerCase();
    }

    /**
     * Sanitizes a file name by removing path traversal characters and illegal path separators.
     */
    public static String sanitizeFileName(String fileName) {
        if (fileName == null) {
            return "";
        }
        // Remove path traversal sequences and separators
        String clean = fileName.replaceAll("[\\\\/]+", "_")
                .replaceAll("\\.\\.+", ".")
                .trim();
        return clean.replaceAll("[^a-zA-Z0-9_.-]", "_");
    }

    /**
     * Formats raw bytes into human-readable representation (e.g. 1024 -> "1 KB", 1048576 -> "1 MB").
     */
    public static String formatFileSize(long bytes) {
        if (bytes <= 0) {
            return "0 B";
        }
        int digitGroups = (int) (Math.log10(bytes) / Math.log10(1024));
        if (digitGroups >= SIZE_UNITS.length) {
            digitGroups = SIZE_UNITS.length - 1;
        }
        return new DecimalFormat("#,##0.#", DecimalFormatSymbols.getInstance(Locale.ENGLISH))
                .format(bytes / Math.pow(1024, digitGroups)) + " " + SIZE_UNITS[digitGroups];
    }

    /**
     * Checks whether the file size is within acceptable threshold.
     */
    public static boolean isValidFileSize(long bytes, long maxBytes) {
        return bytes > 0 && bytes <= maxBytes;
    }
}
