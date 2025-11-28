@echo off
cls
echo.
echo ==========================================
echo   SecureAI-MedGenomics Platform
echo   Starting Backend Server...
echo ==========================================
echo.

REM Kill any existing process on port 8000
echo [*] Checking port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo [*] Killing existing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo [*] Port 8000 is now free
echo.

REM Start backend
cd /d "%~dp0backend"

echo [*] Starting integrated backend...
echo [*] Press Ctrl+C to stop
echo.
echo ==========================================
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Health: http://localhost:8000/api/health
echo ==========================================
echo.

"C:\Users\YAHOO COMPUTER\AppData\Local\Programs\Python\Python311\python.exe" integrated_main.py

pause
