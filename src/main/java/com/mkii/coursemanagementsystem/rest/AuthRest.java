package com.mkii.coursemanagementsystem.rest;

import com.mkii.coursemanagementsystem.dto.auth.AuthResponse;
import com.mkii.coursemanagementsystem.dto.auth.LoginRequest;
import com.mkii.coursemanagementsystem.dto.auth.RegisterRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@RequestMapping("/api/auth")
public interface AuthRest {

    @PostMapping("/login")
    ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request);

    @PostMapping("/register")
    ResponseEntity<AuthResponse> register(@RequestBody RegisterRequest request);

    @GetMapping("/me")
    ResponseEntity<AuthResponse> getCurrentUser(Authentication authentication);
}
