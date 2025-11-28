@echo off
REM ==========================================
REM SecureAI-MedGenomics Platform Launcher
REM Automated Startup Script for Windows
REM ==========================================

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║     SecureAI-MedGenomics Platform - Startup Script           ║
echo ║     7-Layer Security Architecture for Genomic Data           ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo ✅ Python found
echo.

REM Check Node.js installation (optional, for http-server)
echo [2/6] Checking Node.js and http-server...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found - will use Python HTTP server
    set USE_NODE=0
) else (
    node --version
    http-server --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  http-server not installed - will use Python HTTP server
        set USE_NODE=0
    ) else (
        echo ✅ Node.js and http-server found
        set USE_NODE=1
    )
)
echo.

REM Check backend dependencies
echo [3/6] Checking backend dependencies...
cd /d "%~dp0backend"

if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies ready
echo.

REM Check database
echo [4/6] Checking database...
if not exist "genomic_data.db" (
    echo 📊 Database will be created on first run
) else (
    echo ✅ Database found: genomic_data.db
)

if not exist "encrypted\" (
    mkdir encrypted
    echo 📁 Created encrypted storage folder
)
echo.

REM Start Backend Server
echo [5/6] Starting Backend Server (FastAPI on port 8000)...
echo Starting INTEGRATED backend with AI + Security...
start "SecureAI-MedGenomics Backend (Port 8000)" cmd /k "cd /d "%~dp0backend" && "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" integrated_main.py"
echo ✅ Backend server starting...
echo Waiting 8 seconds for backend to initialize...
timeout /t 8 /nobreak >nul
echo.

REM Start Frontend Server
echo [6/6] Starting Frontend Server (Port 3000)...
cd /d "%~dp0frontend"

if "%USE_NODE%"=="1" (
    echo Using http-server...
    start "SecureAI-MedGenomics Frontend (Port 3000)" cmd /k "cd /d "%~dp0frontend" && http-server -p 3000 -c-1"
) else (
    echo Using Python HTTP server...
    start "SecureAI-MedGenomics Frontend (Port 3000)" cmd /k "cd /d "%~dp0frontend" && python -m http.server 3000"
)
echo ✅ Frontend server starting...
echo.

echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    🚀 PLATFORM READY!                         ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📍 Backend API:  http://localhost:8000
echo 📍 Frontend UI:  http://localhost:3000
echo 📊 API Docs:     http://localhost:8000/docs
echo 📊 Health Check: http://localhost:8000/health
echo.
echo ⚡ Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

start http://localhost:3000

echo.
echo ✅ Platform is running!
echo.
echo 📝 To stop the servers:
echo    - Close the terminal windows
echo    - Or press Ctrl+C in each terminal
echo.
echo 🔐 Security Features Active:
echo    ✓ Genetic Algorithm Optimization
echo    ✓ Genomics-Based Authentication
echo    ✓ Intrusion Detection System (IDS)
echo    ✓ Privacy-Preserving Computation
echo    ✓ Adversarial ML Defense (AML)
echo    ✓ Cryfa Encryption (AES-256)
echo    ✓ Real-Time Monitoring
echo.
echo Press any key to exit this launcher (servers will continue running)...
pause >nul
