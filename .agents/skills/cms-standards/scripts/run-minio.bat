@echo off
setlocal
echo ===================================================
echo [CMS] Starting MinIO Native Server
echo S3 API: http://localhost:9000
echo Console UI: http://localhost:9001
echo User: minioadmin / Password: minioadmin
echo ===================================================

set MINIO_DIR=C:\Users\24110\Downloads\minio
set MINIO_DATA=C:\Users\24110\Downloads\minio\data

if not exist "%MINIO_DATA%" (
    mkdir "%MINIO_DATA%"
)

set MINIO_ROOT_USER=minioadmin
set MINIO_ROOT_PASSWORD=minioadmin

"%MINIO_DIR%\minio.exe" server "%MINIO_DATA%" --console-address ":9001"
endlocal
