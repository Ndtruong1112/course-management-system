@echo off
setlocal
chcp 65001 > nul
title Khoi dong he thong Course Management System (Khong dung Docker)

echo ======================================================================
echo   KHOI DONG HE THONG TRUC TIEP TREN MAY (KHONG DUNG DOCKER)
echo   - Tiet kiem toi da RAM va bo nho o dia
echo ======================================================================
echo.

cd /d "%~dp0"

REM Tu dong thiet lap JDK 21
if exist "C:\Users\Admin\.jdks\openjdk-26.0.2.1" (
    set "JAVA_HOME=C:\Users\Admin\.jdks\openjdk-26.0.2.1"
)

echo [1/2] Dang khoi chay Backend Spring Boot (Port 8080)...
start "Backend Spring Boot" cmd /k "set JAVA_HOME=C:\Users\Admin\.jdks\openjdk-26.0.2.1&& .\mvnw.cmd spring-boot:run"

echo [2/2] Dang khoi chay Chatbot AI Copilot (Port 7860)...
start "Chatbot AI Copilot" cmd /k "cd chatbot && python web_app.py"

echo.
echo ======================================================================
echo   DA KHOI DONG XONG 2 CUA SO RIENG BIET:
echo   - Cua so 1: Backend Java (http://localhost:8080/api/courses)
echo   - Cua so 2: Chatbot AI   (http://localhost:7860)
echo.
echo   * Trinh duyet web se tu dong bat len tab Chatbot trong vai giay!
echo ======================================================================
ping 127.0.0.1 -n 3 > nul
