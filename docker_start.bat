@echo off
setlocal
chcp 65001 > nul
title Khoi dong Course Management System bang Docker Compose

echo ======================================================================
echo   KHOI DONG TOAN BO HE THONG BANG DOCKER COMPOSE
echo ======================================================================
echo.

cd /d "%~dp0"

REM Tu dong nap duong dan Docker vao phien lam viec
where docker >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin;%PATH%"
    )
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        set "PATH=C:\Program Files\Docker\Docker\resources\bin;%PATH%"
    )
)

echo [1/3] Kiem tra Docker Daemon...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI]: Khong the ket noi toi Docker CLI!
    echo Vui long dam bao Docker Desktop da duoc bat va dang chay.
    pause
    exit /b 1
)

echo [2/3] Dang build va khoi chay cac container (MySQL, MinIO, Backend, Chatbot)...
docker compose up -d --build

echo.
echo [3/3] Kiem tra trang thai cac dich vu:
docker compose ps

echo.
echo ======================================================================
echo   HE THONG DA DUOC KHOI CHAY HOAN TAT TRONG CONTAINER:
echo   - Backend Spring Boot:   http://localhost:8080
echo   - Chatbot Trợ Lý AI Nội Bộ:    http://localhost:7860
echo   - MinIO Object Storage:  http://localhost:9000 (API)
echo   - MinIO Console UI:      http://localhost:9001 (minioadmin / minioadmin)
echo   - MySQL Database:        localhost:3306 (course_db, pass: 123456)
echo ======================================================================
echo.
pause
