# Universal Spring Boot Agent Prompt & Portability Guide

Tài liệu này hướng dẫn cách sao chép và nhúng bộ kỹ năng **`springboot-standards`** vào **bất kỳ dự án Spring Boot nào khác**, cũng như tích hợp với **mọi Coding Agent AI** trên thị trường (Cursor, Claude Code, Windsurf, GitHub Copilot, Roo Code, Aider, ChatGPT, v.v.).

---

## 1. Cách xuất và sử dụng bộ Skill cho Dự án Mới (Portability)

Để áp dụng toàn bộ quy chuẩn này cho một dự án Spring Boot mới, chỉ cần sao chép toàn bộ thư mục `.agents/skills/springboot-standards` vào thư mục gốc của dự án mới:

```bash
# Ví dụ sao chép sang dự án mới
cp -r .agents/skills/springboot-standards /path/to/new-spring-boot-project/.agents/skills/
```

Mọi Coding Agent hỗ trợ chuẩn Agent Skill (như Antigravity) sẽ tự động phát hiện và kích hoạt bộ quy chuẩn này ngay khi bạn mở dự án.

---

## 2. File cấu hình sẵn cho các Coding Agent phổ biến

Dưới đây là nội dung sẵn sàng để copy-paste vào file cấu hình riêng của từng Agent:

### A. Đối với Cursor (`.cursorrules` hoặc `.cursor/rules/spring-boot.mdc`)
Tạo file `.cursorrules` ở thư mục gốc của dự án:
```markdown
# Spring Boot Engineering Rules for Cursor

You are an expert Spring Boot software engineer. When writing, refactoring, or reviewing code in this project, you MUST strictly follow the standards defined in `.agents/skills/springboot-standards/SKILL.md`:

1. Strict 3-layer architecture: Controller -> Service (Interface + Impl) -> Repository. Controller NEVER calls Repository directly.
2. DTO Isolation: NEVER expose JPA Entities to Controller or API responses. Always use Request/Response DTOs and Mappers.
3. Uniform API Envelope: Wrap all REST responses in `ApiResponse<T>` or `PageResponse<T>`.
4. No Hardcoded Strings: All error messages, exception messages, and success texts MUST be centralized in `common.MessageConstants`.
5. Constructor Injection: NEVER use field `@Autowired`. Use `private final` fields with `@RequiredArgsConstructor`.
6. Transaction Boundaries: Use `@Transactional(readOnly = true)` at class level, and `@Transactional` on write methods.
7. Zero N+1 Queries: Always use `@EntityGraph` or `JOIN FETCH` for relationships. Keep `open-in-view: false`.
8. Testing: Only write/run tests when explicitly requested by the user.
```

---

### B. Đối với Claude Code (`CLAUDE.md`)
Tạo file `CLAUDE.md` ở thư mục gốc của dự án:
```markdown
# Claude Code Project Guidelines - Spring Boot Standards

- Architectural standard: Follow the guidelines in `.agents/skills/springboot-standards/SKILL.md`.
- Always use interface-driven development for Services (`service/I{Entity}Service.java` and `service/impl/{Entity}ServiceImpl.java`).
- Never return Entity instances from REST endpoints; use DTOs only.
- Centralize all messages and exception strings in `package com.{company}.{project}.common.MessageConstants`.
- Never modify skills or write tests unless explicitly instructed by the user.
- Build verification: Run `./mvnw test-compile` to check compilation.
```

---

### C. Đối với Windsurf (`.windsurfrules`)
Tạo file `.windsurfrules` ở thư mục gốc:
```markdown
Strictly adhere to the Spring Boot architectural standards defined in `.agents/skills/springboot-standards/SKILL.md`.
Key constraints:
- Controller -> Service Interface -> Service Impl -> Repository.
- DTO & Entity complete separation.
- No string literals in exception throws; import and use `MessageConstants`.
- Constructor injection only.
```

---

### D. Đối với GitHub Copilot (`.github/copilot-instructions.md`)
Tạo file `.github/copilot-instructions.md`:
```markdown
When generating Java Spring Boot code:
- Ensure 3-tier layering with Service Interfaces.
- Use Lombok `@RequiredArgsConstructor` for constructor injection.
- Use `ApiResponse<T>` wrapper for controllers.
- Look up existing constants in `MessageConstants` before generating exception strings.
```

---

## 3. Master Prompt dùng trực tiếp trong Chat (Dành cho mọi Agent)

Nếu bạn sử dụng bất kỳ AI Chat hoặc Web UI nào, hãy copy đoạn System Prompt dưới đây để yêu cầu Agent tuân thủ:

```text
Bạn là một chuyên gia cao cấp về Spring Boot. Khi bạn làm việc với codebase này, bạn bắt buộc phải tuân theo 10 nguyên tắc vàng sau:
1. Luôn tuân thủ kiến trúc phân tầng nghiêm ngặt (Controller -> Service Interface -> Service Impl -> Repository).
2. Tuyệt đối không để JPA Entity rò rỉ ra ngoài API response; luôn dùng Request/Response DTO và Mapper.
3. Mọi endpoint REST phải trả về cấu trúc chuẩn ApiResponse<T> hoặc PageResponse<T>.
4. Không bao giờ hardcode chuỗi thông báo hay exception message; toàn bộ phải khai báo tập trung trong package common (MessageConstants).
5. Luôn dùng Constructor Injection kết hợp private final và Lombok @RequiredArgsConstructor; tuyệt đối không dùng field @Autowired.
6. Luôn khai báo @Transactional(readOnly = true) ở cấp độ class Service và @Transactional cho các hàm ghi/xóa dữ liệu.
7. Triệt tiêu hoàn toàn lỗi N+1 Query bằng cách dùng @EntityGraph hoặc JOIN FETCH; đặt open-in-view: false.
8. Kiểm tra dữ liệu tại ranh giới Controller bằng Bean Validation (@Valid).
9. Quản lý cấu hình đa môi trường an toàn qua application.yml và biến môi trường, không commit secret vào code.
10. Chỉ viết hoặc cập nhật unit test khi có yêu cầu trực tiếp từ tôi.
```
