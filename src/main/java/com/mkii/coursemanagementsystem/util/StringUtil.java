package com.mkii.coursemanagementsystem.util;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

/**
 * Technical helper utility providing static methods for string manipulation,
 * sensitive data masking, slug generation, and validation checks.
 * Contains purely technical methods without any business logic.
 */
public final class StringUtil {

    private static final Pattern NON_LATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");

    private StringUtil() {
        throw new UnsupportedOperationException("Utility class cannot be instantiated");
    }

    public static boolean isEmpty(CharSequence cs) {
        return cs == null || cs.length() == 0;
    }

    public static boolean isNotEmpty(CharSequence cs) {
        return !isEmpty(cs);
    }

    public static boolean isBlank(CharSequence cs) {
        if (cs == null) {
            return true;
        }
        for (int i = 0; i < cs.length(); i++) {
            if (!Character.isWhitespace(cs.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public static boolean isNotBlank(CharSequence cs) {
        return !isBlank(cs);
    }

    /**
     * Masks sensitive string content, keeping a prefix and suffix visible.
     * Example: maskSensitive("mysecrettoken123", 3, 3) -> "mys**********123"
     */
    public static String maskSensitive(String input, int startVisible, int endVisible) {
        if (input == null) {
            return null;
        }
        int len = input.length();
        if (len <= (startVisible + endVisible)) {
            return "*".repeat(len);
        }
        String prefix = input.substring(0, startVisible);
        String suffix = input.substring(len - endVisible);
        String masked = "*".repeat(len - startVisible - endVisible);
        return prefix + masked + suffix;
    }

    /**
     * Masks an email address for privacy.
     * Example: "student@example.com" -> "s***t@example.com"
     */
    public static String maskEmail(String email) {
        if (email == null || !email.contains("@")) {
            return maskSensitive(email, 1, 1);
        }
        String[] parts = email.split("@", 2);
        String name = parts[0];
        String domain = parts[1];
        if (name.length() <= 2) {
            return "*".repeat(name.length()) + "@" + domain;
        }
        return name.charAt(0) + "*".repeat(name.length() - 2) + name.charAt(name.length() - 1) + "@" + domain;
    }

    /**
     * Generates a clean URL slug from text (supporting Vietnamese diacritics).
     * Example: "Khóa học Lập trình Java 2026!" -> "khoa-hoc-lap-trinh-java-2026"
     */
    public static String toSlug(String input) {
        if (input == null || input.trim().isEmpty()) {
            return "";
        }
        String normalized = Normalizer.normalize(input, Normalizer.Form.NFD);
        String noDiacritics = Pattern.compile("\\p{InCombiningDiacriticalMarks}+").matcher(normalized).replaceAll("");
        noDiacritics = noDiacritics.replace("đ", "d").replace("Đ", "D");
        String noWhitespace = WHITESPACE.matcher(noDiacritics).replaceAll("-");
        String slug = NON_LATIN.matcher(noWhitespace).replaceAll("");
        return slug.toLowerCase(Locale.ENGLISH).replaceAll("-+", "-").replaceAll("^-|-$", "");
    }
}
