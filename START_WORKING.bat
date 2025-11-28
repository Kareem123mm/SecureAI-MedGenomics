@echo off
title SecureAI-MedGenomics - Quick Start
color 0A

echo.
echo ==========================================
echo   SecureAI-MedGenomics Platform
echo   Quick Start Script
echo ==========================================
echo.

REM Kill any existing Python processes on port 8000
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [*] Starting backend server...
cd /d "%~dp0backend"

REM Start backend in new window
start "SecureAI Backend" cmd /k ""C:\Users\YAHOO COMPUTER\AppData\Local\Programs\Python\Python311\python.exe" integrated_main.py"

echo.
echo [*] Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo   Backend is running!
echo ==========================================
echo.
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Health:   http://localhost:8000/api/health
echo.
echo ==========================================
echo.
echo [*] Opening API documentation in browser...
start http://localhost:8000/docs

echo.
echo Press any key to open frontend...
pause >nul

REM Open frontend
start http://localhost:8000
cd ..
start frontend\index.html

echo.
echo ==========================================
echo   System is ready!
echo ==========================================
echo.
pause
