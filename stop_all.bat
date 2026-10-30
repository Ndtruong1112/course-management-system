@echo off
setlocal
chcp 65001 > nul
title Dung he thong Course Management System

echo ======================================================================
echo   DUNG HE THONG COURSE MANAGEMENT SYSTEM (PORT 8080 VA 7860)
echo ======================================================================
echo.

echo Dang dung Backend Spring Boot (Port 8080)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo Dang dung Chatbot AI Copilot (Port 7860)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :7860 ^| findstr LISTENING') do (
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo ======================================================================
echo   DA TAT THANH CONG CAC TIEN TRINH BACKEND VA CHATBOT!
echo ======================================================================
pause
