# 05. Bảo mật & Quản lý Cấu hình Đa môi trường

Tài liệu này cung cấp các tiêu chuẩn bảo mật hiện đại với Spring Security 6+ (Spring Boot 3.x) và phương pháp quản trị cấu hình đa môi trường an toàn.

---

## 1. Cấu hình Spring Security 6+ Component-Based (`SecurityFilterChain`)

Kể từ Spring Boot 3 / Spring Security 6, `WebSecurityConfigurerAdapter` đã bị loại bỏ hoàn toàn. Mọi cấu hình bảo mật được khai báo dưới dạng Spring Beans:

```java
package com.company.project.config;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
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
@EnableMethodSecurity // Kích hoạt @PreAuthorize trên Service/Controller
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final CustomAuthenticationEntryPoint authenticationEntryPoint;
    private final CustomAccessDeniedHandler accessDeniedHandler;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // 1. Tắt CSRF vì ứng dụng REST sử dụng Token Stateless
            .csrf(AbstractHttpConfigurer::disable)
            
            // 2. Kích hoạt cấu hình CORS chuẩn
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            
            // 3. Quản lý Session là STATELESS (Không lưu session trên server)
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            
            // 4. Xử lý Exception xác thực tập trung
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(authenticationEntryPoint)
                .accessDeniedHandler(accessDeniedHandler)
            )
            
            // 5. Phân quyền Endpoint
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(
                    "/api/v1/auth/**",
                    "/v3/api-docs/**",
                    "/swagger-ui/**",
                    "/swagger-ui.html",
                    "/actuator/health"
                ).permitAll()
                .anyRequest().authenticated()
            )
            
            // 6. Thêm JWT Filter trước filter mặc định của Spring
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(List.of("*"));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type", "X-Requested-With", "Accept"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L); // Cache kết quả Preflight trong 1 giờ

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

---

## 2. Quản lý Cấu hình Đa môi trường (`application.yml`)

### Cấu trúc phân tách file:
```text
src/main/resources/
├── application.yml         # Cấu hình chung cơ sở (tên app, profile mặc định)
├── application-dev.yml     # Môi trường phát triển cục bộ (H2/Local MySQL, verbose log)
├── application-staging.yml # Môi trường kiểm thử
└── application-prod.yml    # Môi trường chạy thật (Bảo mật cao, tắt debug, connection pool lớn)
```

### Quy tắc bảo mật cấu hình (Externalized Configuration):
**TUYỆT ĐỐI KHÔNG commit mật khẩu hoặc khóa bí mật vào Git repository.** Sử dụng biến môi trường với giá trị fallback an toàn cho môi trường dev:

```yaml
# application.yml mẫu
spring:
  application:
    name: course-management-system
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

app:
  jwt:
    secret: ${JWT_SECRET:LocalDevelopmentSecretKeyWithAtLeast256BitsLengthForTesting1234567890}
    expiration-ms: ${JWT_EXPIRATION_MS:86400000} # 24 giờ
```

---

## 3. Cấu hình Type-Safe với `@ConfigurationProperties`

Tránh sử dụng rải rác `@Value("${...}")`. Gom nhóm cấu hình vào các bean có kiểm tra tính hợp lệ (Validation):

```java
package com.company.project.config.properties;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@Configuration
@ConfigurationProperties(prefix = "app.jwt")
public class JwtProperties {

    @NotBlank(message = "JWT Secret must not be blank")
    private String secret;

    @Positive(message = "JWT Expiration must be positive")
    private long expirationMs;
}
```
