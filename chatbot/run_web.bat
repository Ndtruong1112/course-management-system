@echo off
chcp 65001 > nul
title Course Management System - AI Chatbot Web UI
echo ======================================================================
echo   KHỞI ĐỘNG GIAO DIỆN CHATBOT (BASE MODEL vs FINE-TUNED MODEL)
echo ======================================================================
echo.
cd /d "%~dp0"
python web_app.py
pause
