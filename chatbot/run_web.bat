@echo off
setlocal
chcp 65001 > nul
title Course Management System - AI Chatbot Web UI
echo ======================================================================
echo   KHỞI ĐỘNG GIAO DIỆN CHATBOT (BASE MODEL vs FINE-TUNED MODEL)
echo ======================================================================
echo.

cd /d "%~dp0"

REM Giai phong port 7860 neu dang bi chiem dung
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :7860 ^| findstr LISTENING') do (
    echo [THONG BAO] Dang giai phong port 7860 cu (PID: %%a)...
    taskkill /f /pid %%a >nul 2>&1
)

python web_app.py
pause
