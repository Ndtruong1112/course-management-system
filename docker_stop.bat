@echo off
setlocal
chcp 65001 > nul
title Dung Course Management System tren Docker

echo ======================================================================
echo   DANG DUNG TOAN BO HE THONG CONTAINER DOCKER
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

docker compose down

echo.
echo Da dung va giai phong toan bo container. (Du lieu MySQL va MinIO van duoc giu nguyen trong Volume).
pause
