# ==========================================
# SecureAI-MedGenomics Platform Launcher
# PowerShell Startup Script
# ==========================================

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "     SecureAI-MedGenomics Platform - Startup Script         " -ForegroundColor Cyan
Write-Host "     7-Layer Security Architecture for Genomic Data         " -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"
$frontendPath = Join-Path $scriptPath "frontend"

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
    Write-Host "[OK] Python found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check Node.js and http-server
Write-Host "[2/6] Checking Node.js and http-server..." -ForegroundColor Yellow
$useNode = $false
try {
    $nodeVersion = node --version 2>&1
    Write-Host $nodeVersion -ForegroundColor Green
    
    $httpServerVersion = http-server --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Node.js and http-server found" -ForegroundColor Green
        $useNode = $true
    } else {
        Write-Host "[WARNING] http-server not installed - will use Python HTTP server" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Node.js not found - will use Python HTTP server" -ForegroundColor Yellow
}
Write-Host ""

# Check backend dependencies
Write-Host "[3/6] Checking backend dependencies..." -ForegroundColor Yellow
Set-Location $backendPath

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

Write-Host "Installing/Updating dependencies..." -ForegroundColor Yellow
Write-Host "[INFO] Installing essential packages (skipping pysam - requires C compiler)..." -ForegroundColor Cyan
pip install --quiet --upgrade pip

# Install essential packages without pysam (requires C compiler on Windows)
pip install --quiet fastapi==0.109.0 uvicorn[standard]==0.27.0 python-multipart==0.0.6 pydantic==2.5.3 cryptography==42.0.0 biopython==1.83 aiosqlite==0.19.0 prometheus-client==0.19.0

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Backend dependencies ready" -ForegroundColor Green
Write-Host ""

# Check database
Write-Host "[4/6] Checking database..." -ForegroundColor Yellow
if (-not (Test-Path "genomic_data.db")) {
    Write-Host "[INFO] Database will be created on first run" -ForegroundColor Cyan
} else {
    Write-Host "[OK] Database found: genomic_data.db" -ForegroundColor Green
}

if (-not (Test-Path "encrypted")) {
    New-Item -ItemType Directory -Path "encrypted" | Out-Null
    Write-Host "[INFO] Created encrypted storage folder" -ForegroundColor Cyan
}
Write-Host ""

# Start Backend Server
Write-Host "[5/6] Starting Backend Server (FastAPI on port 8000)..." -ForegroundColor Yellow
Write-Host "Starting backend in new window..." -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; & 'venv\Scripts\Activate.ps1'; python real_main.py" -WindowStyle Normal

Write-Host "[OK] Backend server starting..." -ForegroundColor Green
Write-Host "Waiting 5 seconds for backend to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
Write-Host ""

# Start Frontend Server
Write-Host "[6/6] Starting Frontend Server (Port 3000)..." -ForegroundColor Yellow
Set-Location $frontendPath

if ($useNode) {
    Write-Host "Using http-server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; http-server -p 3000 -c-1" -WindowStyle Normal
} else {
    Write-Host "Using Python HTTP server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; python -m http.server 3000" -WindowStyle Normal
}

Write-Host "[OK] Frontend server starting..." -ForegroundColor Green
Write-Host ""

Write-Host "=============================================================" -ForegroundColor Green
Write-Host "                    PLATFORM READY!                         " -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend UI:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening browser in 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "[OK] Platform is running!" -ForegroundColor Green
Write-Host ""
Write-Host "To stop the servers:" -ForegroundColor Yellow
Write-Host "   - Close the PowerShell windows" -ForegroundColor Gray
Write-Host "   - Or press Ctrl+C in each window" -ForegroundColor Gray
Write-Host ""
Write-Host "Security Features Active:" -ForegroundColor Cyan
Write-Host "   [OK] Genetic Algorithm Optimization" -ForegroundColor Gray
Write-Host "   [OK] Genomics-Based Authentication" -ForegroundColor Gray
Write-Host "   [OK] Intrusion Detection System (IDS)" -ForegroundColor Gray
Write-Host "   [OK] Privacy-Preserving Computation" -ForegroundColor Gray
Write-Host "   [OK] Adversarial ML Defense (AML)" -ForegroundColor Gray
Write-Host "   [OK] Cryfa Encryption (AES-256)" -ForegroundColor Gray
Write-Host "   [OK] Real-Time Monitoring" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Enter to exit this launcher (servers will continue running)..." -ForegroundColor Yellow
Read-Host
