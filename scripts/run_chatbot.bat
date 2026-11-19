@echo off
setlocal
chcp 65001 > nul
title Course Management System - AI Chatbot Web UI
echo ======================================================================
echo   KHỞI ĐỘNG GIAO DIỆN CHATBOT (BASE MODEL vs FINE-TUNED MODEL)
echo ======================================================================
echo.

cd /d "%~dp0..\chatbot"

REM Khong tu y dung tien trinh khac dang su dung port.
powershell -NoProfile -Command "try { $c = New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1', 7860); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo [LOI] Port 7860 dang duoc su dung. Hay kiem tra truoc khi chay.
    exit /b 1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :7860 ^| findstr LISTENING') do (
    echo [LOI] Port 7860 dang duoc su dung boi PID %%a. Hay kiem tra truoc khi chay.
    pause
    exit /b 1
)

python web_app.py
pause
