@echo off
setlocal
chcp 65001 > nul
title Khoi dong he thong Course Management System (Khong dung Docker)

echo ======================================================================
echo   KHOI DONG HE THONG TRUC TIEP TREN MAY (KHONG DUNG DOCKER)
echo   - Tiet kiem toi da RAM va bo nho o dia
echo ======================================================================
echo.

cd /d "%~dp0.."

REM Tu dong thiet lap JAVA_HOME neu may chua cau hinh
if not defined JAVA_HOME (
    if exist "C:\Users\Admin\.jdks\openjdk-26.0.2.1" (
        set "JAVA_HOME=C:\Users\Admin\.jdks\openjdk-26.0.2.1"
    )
)

echo [1/2] Dang khoi chay Backend Spring Boot (Port 8080)...
start "Backend Spring Boot" cmd /k "cd /d "%~dp0.." && .\mvnw.cmd spring-boot:run"

echo [2/2] Dang khoi chay Tro Ly AI Noi Bo (Port 7860)...
start "Tro Ly AI Noi Bo" cmd /k "cd chatbot && python web_app.py"

echo.
echo ======================================================================
echo   DA KHOI DONG XONG 2 CUA SO RIENG BIET:
echo   - Cua so 1: Backend Java (http://localhost:8080/api/courses)
echo   - Cua so 2: Chatbot AI   (http://localhost:7860)
echo.
echo   * Trinh duyet web dang tu dong mo giao dien Chatbot AI...
echo ======================================================================
timeout /t 5 /nobreak >nul 2>&1 || ping 127.0.0.1 -n 6 >nul
start http://localhost:7860
