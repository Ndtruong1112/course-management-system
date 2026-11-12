package com.mkii.coursemanagementsystem.config;

import com.mkii.coursemanagementsystem.security.jwt.JwtAccessDeniedHandler;
import com.mkii.coursemanagementsystem.security.jwt.JwtAuthenticationEntryPoint;
import com.mkii.coursemanagementsystem.security.jwt.JwtAuthenticationFilter;
import com.mkii.coursemanagementsystem.security.jwt.JwtTokenProvider;
import com.mkii.coursemanagementsystem.security.service.UserDetailsServiceImpl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;
import java.util.List;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    private final UserDetailsServiceImpl userDetailsService;
    private final JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint;
    private final JwtAccessDeniedHandler jwtAccessDeniedHandler;
    private final JwtTokenProvider jwtTokenProvider;

    public SecurityConfig(@Lazy UserDetailsServiceImpl userDetailsService,
                          JwtAuthenticationEntryPoint jwtAuthenticationEntryPoint,
                          JwtAccessDeniedHandler jwtAccessDeniedHandler,
                          JwtTokenProvider jwtTokenProvider) {
        this.userDetailsService = userDetailsService;
        this.jwtAuthenticationEntryPoint = jwtAuthenticationEntryPoint;
        this.jwtAccessDeniedHandler = jwtAccessDeniedHandler;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(List.of("*"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type", "X-Requested-With", "Accept", "Origin"));
        configuration.setExposedHeaders(Arrays.asList("Authorization", "Content-Type"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(jwtAuthenticationEntryPoint)
                .accessDeniedHandler(jwtAccessDeniedHandler)
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authorizeHttpRequests(auth -> auth
                // Public giao diện Web tĩnh (Frontend)
                .requestMatchers("/", "/index.html", "/favicon.ico", "/*.html", "/*.css", "/*.js", "/static/**", "/error").permitAll()
                // Public tài liệu Swagger / OpenAPI
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**", "/swagger-ui.html", "/swagger-resources/**", "/webjars/**").permitAll()
                // Public các API xác thực (Đăng nhập, Đăng ký) và thống kê tổng quan không chứa PII
                .requestMatchers("/api/auth/**", "/api/dashboard/**").permitAll()
                // Cho phép xem thông tin khóa học và khoa công khai không cần token (A3)
                .requestMatchers(HttpMethod.GET, "/api/courses/**", "/api/departments/**").permitAll()
                // Cho phép CORS preflight
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                // Quyền ghi đối với khóa học và khoa (ADMIN, TEACHER, LECTURER) (A4)
                .requestMatchers(HttpMethod.POST, "/api/courses/**", "/api/departments/**", "/api/enrollments/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.PUT, "/api/courses/**", "/api/departments/**", "/api/enrollments/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.DELETE, "/api/courses/**", "/api/departments/**", "/api/enrollments/**").hasRole("ADMIN")
                // Quyền ghi đối với sinh viên
                .requestMatchers(HttpMethod.POST, "/api/students/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.PUT, "/api/students/**").hasAnyRole("ADMIN", "TEACHER", "LECTURER")
                .requestMatchers(HttpMethod.DELETE, "/api/students/**").hasRole("ADMIN")
                // Mọi thao tác khác (kể cả GET sinh viên PII, GET/POST tài liệu nội bộ) bắt buộc phải đăng nhập (A3, A4)
                .anyRequest().authenticated()
            );

        JwtAuthenticationFilter jwtAuthenticationFilter = new JwtAuthenticationFilter(jwtTokenProvider, userDetailsService);
        http.authenticationProvider(authenticationProvider());
        http.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
