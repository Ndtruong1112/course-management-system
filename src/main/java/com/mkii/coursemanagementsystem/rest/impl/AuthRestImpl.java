package com.mkii.coursemanagementsystem.rest.impl;

import com.mkii.coursemanagementsystem.common.exception.BadRequestException;
import com.mkii.coursemanagementsystem.common.exception.ResourceNotFoundException;
import com.mkii.coursemanagementsystem.dao.IUserDao;
import com.mkii.coursemanagementsystem.dto.auth.AuthResponse;
import com.mkii.coursemanagementsystem.dto.auth.LoginRequest;
import com.mkii.coursemanagementsystem.dto.auth.RegisterRequest;
import com.mkii.coursemanagementsystem.entity.User;
import com.mkii.coursemanagementsystem.rest.AuthRest;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuthRestImpl implements AuthRest {

    private static final Logger logger = LoggerFactory.getLogger(AuthRestImpl.class);

    private final AuthenticationManager authenticationManager;
    private final IUserDao userDao;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider tokenProvider;

    public AuthRestImpl(AuthenticationManager authenticationManager,
                        IUserDao userDao,
                        PasswordEncoder passwordEncoder,
                        JwtTokenProvider tokenProvider) {
        this.authenticationManager = authenticationManager;
        this.userDao = userDao;
        this.passwordEncoder = passwordEncoder;
        this.tokenProvider = tokenProvider;
    }

    @Override
    public ResponseEntity<AuthResponse> login(@Valid LoginRequest request) {
        logger.info("Attempting login for user: {}", request.getUsername());

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        User user = userDao.findByUsername(request.getUsername())
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + request.getUsername()));

        AuthResponse response = AuthResponse.builder()
                .token(jwt)
                .userId(user.getUserId())
                .username(user.getUsername())
                .email(user.getEmail())
                .fullName(user.getFullName())
                .role(user.getRole())
                .build();

        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<AuthResponse> register(@Valid RegisterRequest request) {
        logger.info("Registering new user: {}", request.getUsername());

        if (userDao.existsByUsername(request.getUsername())) {
            throw new BadRequestException("Username đã tồn tại: " + request.getUsername());
        }

        if (request.getEmail() != null && userDao.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email đã tồn tại: " + request.getEmail());
        }

        // Quyền mặc định khi tự đăng ký luôn là USER để ngăn chặn leo thang đặc quyền (A2)
        String role = "USER";

        User user = User.builder()
                .username(request.getUsername().trim())
                .password(passwordEncoder.encode(request.getPassword()))
                .email(request.getEmail())
                .fullName(request.getFullName())
                .role(role)
                .build();

        User savedUser = userDao.save(user);

        // Auto login after registration
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername(), request.getPassword())
        );
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = tokenProvider.generateToken(authentication);

        AuthResponse response = AuthResponse.builder()
                .token(jwt)
                .userId(savedUser.getUserId())
                .username(savedUser.getUsername())
                .email(savedUser.getEmail())
                .fullName(savedUser.getFullName())
                .role(savedUser.getRole())
                .build();

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @Override
    public ResponseEntity<AuthResponse> getCurrentUser(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated() 
                || authentication instanceof org.springframework.security.authentication.AnonymousAuthenticationToken) {
            throw new org.springframework.security.authentication.InsufficientAuthenticationException("Vui lòng đăng nhập để thực hiện thao tác");
        }

        String username = authentication.getName();
        User user = userDao.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found: " + username));

        AuthResponse response = AuthResponse.builder()
                .userId(user.getUserId())
                .username(user.getUsername())
                .email(user.getEmail())
                .fullName(user.getFullName())
                .role(user.getRole())
                .build();

        return ResponseEntity.ok(response);
    }
}
