# ==========================================
# STAGE 1: Build ứng dụng Spring Boot
# ==========================================
FROM maven:3.9.6-eclipse-temurin-21 AS builder
WORKDIR /build

# Tận dụng Docker layer cache cho dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy mã nguồn và đóng gói JAR
COPY src ./src
RUN mvn clean package -DskipTests -B

# ==========================================
# STAGE 2: Image runtime gọn nhẹ (Alpine JRE)
# ==========================================
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Thêm người dùng không có quyền root vì mục tiêu bảo mật
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copy file jar từ stage build
COPY --from=builder /build/target/*.jar app.jar

# Mở cổng 8080 cho Spring Boot API
EXPOSE 8080

# Cấu hình biến môi trường JVM tối ưu bộ nhớ cho container
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -Dfile.encoding=UTF-8"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
