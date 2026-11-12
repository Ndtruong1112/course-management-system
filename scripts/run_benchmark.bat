@echo off
setlocal
chcp 65001 > nul
title Danh Gia Thuc Nghiem So Sanh Trợ Lý AI Dự Án

echo ======================================================================
echo   CHƯƠNG TRÌNH ĐÁNH GIÁ THỰC NGHIỆM KHOA HỌC:
echo   - 1. AI Tiêu Chuẩn Bên Ngoài (Cloud AI - Zero Context Chưa Có Kiến Trúc Dự Án)
echo   - 2. Base Model (Mô hình Gốc chưa Fine-tuning)
echo   - 3. Hệ Thống Dự Án (Fine-tuned Model với Ngữ Cảnh Kiến Trúc)
echo ======================================================================
echo.

cd /d "%~dp0..\benchmark"
python benchmark_comparison.py

echo.
echo ======================================================================
echo   ĐÃ TẠO XONG 2 BÁO CÁO:
echo   1. BAO_CAO_SO_SANH_HIEU_QUA.md (Báo cáo Nghiệm thu Học thuật)
echo   2. bao_cao_truc_quan.html (Bảng điều khiển Trực quan & Biểu đồ)
echo.
echo   Đang tự động mở Báo cáo Trực quan trên Trình duyệt web...
echo ======================================================================
start "" "%~dp0..\benchmark\bao_cao_truc_quan.html"
pause
