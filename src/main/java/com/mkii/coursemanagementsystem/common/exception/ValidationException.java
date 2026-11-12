package com.mkii.coursemanagementsystem.common.exception;

/**
 * Custom runtime exception thrown when business or data validation fails.
 * Handled globally by {@link GlobalExceptionHandler} to return HTTP 400 (Bad Request).
 */
public class ValidationException extends RuntimeException {

    public ValidationException(String message) {
        super(message);
    }

    public ValidationException(String message, Throwable cause) {
        super(message, cause);
    }
}
