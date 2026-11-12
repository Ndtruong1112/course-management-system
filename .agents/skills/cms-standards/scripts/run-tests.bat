@echo off
setlocal
echo ===================================================
echo [CMS] Running Maven Unit Tests with JDK 26 / 21+
echo ===================================================

set JAVA_HOME=C:\Users\24110\.jdks\openjdk-26.0.2.1
set PATH=%JAVA_HOME%\bin;%PATH%

cd /d C:\Users\24110\Downloads\course-management-system--master

if "%~1"=="" (
    echo Running all unit tests...
    call mvnw.cmd test
) else (
    echo Running specific test: %~1
    call mvnw.cmd test -Dtest=%~1
)

echo ===================================================
echo Test execution completed with exit code: %ERRORLEVEL%
echo ===================================================
endlocal
