@echo off
setlocal
chcp 65001 > nul
title Course Management System - Backend
cd /d "%~dp0.."

REM Preserve existing Java/Maven settings; the heap limits are overrideable.
if not defined JAVA_HOME if exist "C:\Users\Admin\.jdks\openjdk-26.0.2.1" set "JAVA_HOME=C:\Users\Admin\.jdks\openjdk-26.0.2.1"
if not defined MAVEN_OPTS set "MAVEN_OPTS=-Xmx384m"
if not defined CMS_BACKEND_JVM_ARGS set "CMS_BACKEND_JVM_ARGS=-Xms64m -Xmx512m"

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do (
    echo [LOI] Port 8080 dang duoc su dung boi PID %%a. Hay kiem tra truoc khi chay.
    pause
    exit /b 1
)

echo Dang build backend voi heap Maven toi da 384 MB neu ban chua tu cau hinh MAVEN_OPTS.
call .\mvnw.cmd -DskipTests package
if errorlevel 1 (
    echo [LOI] Build that bai; khong chay file JAR cu.
    pause
    exit /b 1
)
if not exist "target\course-management-system-0.0.1-SNAPSHOT.jar" (
    echo [LOI] Khong tim thay file JAR sau khi build.
    pause
    exit /b 1
)
echo Khoi dong backend, khong khoi dong chatbot. JVM: %CMS_BACKEND_JVM_ARGS%
echo Cau hinh JVM co the doi qua bien CMS_BACKEND_JVM_ARGS.
if defined JAVA_HOME (
    "%JAVA_HOME%\bin\java.exe" %CMS_BACKEND_JVM_ARGS% -jar "target\course-management-system-0.0.1-SNAPSHOT.jar"
) else (
    java %CMS_BACKEND_JVM_ARGS% -jar "target\course-management-system-0.0.1-SNAPSHOT.jar"
)
set "CMS_BACKEND_EXIT=%ERRORLEVEL%"
if not "%CMS_BACKEND_EXIT%"=="0" echo Backend dung voi ma loi %CMS_BACKEND_EXIT%.
pause
exit /b %CMS_BACKEND_EXIT%
