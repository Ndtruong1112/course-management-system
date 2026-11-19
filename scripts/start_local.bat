@echo off
setlocal
chcp 65001 > nul
title Khoi dong Course Management System
cd /d "%~dp0.."

REM Keep the existing demo-data behavior for this local launcher.
set "CMS_DEMO_DATA_ENABLED=true"
REM Avoid opening a second browser tab from inside the chatbot.
set "AUTO_OPEN_BROWSER=false"

echo Dang kiem tra Backend (8080)...
netstat -aon | findstr /R /C:":8080 .*LISTENING" >nul
if errorlevel 1 powershell -NoProfile -Command "try { $c = New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1', 8080); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo Port 8080 dang duoc su dung; giu nguyen tien trinh hien tai.
) else (
    echo Khoi dong backend qua JAR; Maven se thoat sau khi build.
    start "Backend Spring Boot" cmd /k call "%~dp0run_backend.bat"
)

echo Dang kiem tra Chatbot (7860)...
netstat -aon | findstr /R /C:":7860 .*LISTENING" >nul
if errorlevel 1 powershell -NoProfile -Command "try { $c = New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1', 7860); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
if not errorlevel 1 (
    echo Port 7860 dang duoc su dung; giu nguyen tien trinh hien tai.
) else (
    echo Khoi dong chatbot; model local chi duoc nap khi can.
    start "Tro Ly AI" cmd /k call "%~dp0run_chatbot.bat"
)

echo Giao dien chatbot: http://localhost:7860
echo Backend co the can them thoi gian de build va khoi dong.
timeout /t 5 /nobreak >nul 2>&1 || ping 127.0.0.1 -n 6 >nul
start http://localhost:7860
