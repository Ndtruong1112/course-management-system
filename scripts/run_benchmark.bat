@echo off
setlocal
chcp 65001 > nul
title Danh gia AI - Kiem tra nhanh

echo ======================================================================
echo   KIEM TRA NHANH: 1 cau hoi, 4 cau hinh Base/LoRA va co/khong RAG.
echo   Ket qua can duoc danh gia thu cong truoc khi tinh ty le chat luong.
echo ======================================================================
echo.

cd /d "%~dp0..\benchmark"
python evaluate.py run --limit 1 --max-tokens 128
if errorlevel 1 (
    echo Khong co ket qua thanh cong. Vui long kiem tra log.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   Ket qua duoc luu trong benchmark\runs\ theo duong dan da in phia tren.
echo   Xem benchmark\README.md de chay day du va cham ket qua.
echo ======================================================================
pause
