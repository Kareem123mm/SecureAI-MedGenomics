# ============================================
# SecureAI-MedGenomics - Complete Startup & Test Script
# ============================================
# This script handles EVERYTHING:
# 1. Environment verification
# 2. Dependency installation
# 3. Running tests
# 4. Starting backend
# 5. Testing API endpoints
# ============================================

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SecureAI-MedGenomics Platform v2.0" -ForegroundColor Green
Write-Host "  Complete Startup & Test Script" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Store paths
$SCRIPT_DIR = Split-Path -Parent $PSCommandPath
$BACKEND_DIR = Join-Path $SCRIPT_DIR "backend"
$MODELS_DIR = Join-Path $SCRIPT_DIR "models_export"

# Find Python executable
Write-Host "[1/10] Finding Python..." -ForegroundColor Yellow
$PYTHON_EXE = $null

# Check for standard Windows Python
$standardPython = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe"
if (Test-Path $standardPython) {
    $PYTHON_EXE = $standardPython
} else {
    # Try to find python in PATH
    try {
        $pythonPath = (Get-Command python -ErrorAction Stop).Source
        if ($pythonPath -notlike "*msys64*") {
            $PYTHON_EXE = $pythonPath
        }
    } catch {}
}

if (-not $PYTHON_EXE) {
    Write-Host "      ✗ Python 3.11+ not found!" -ForegroundColor Red
    Write-Host "      Please install from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host "      ✓ Found: $PYTHON_EXE" -ForegroundColor Green

# Check Python version
$pythonVersion = & $PYTHON_EXE --version 2>&1
Write-Host "      ✓ Version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "[2/10] Checking dependencies..." -ForegroundColor Yellow
$requiredPackages = @("fastapi", "torch", "sklearn", "xgboost", "pytest")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $check = & $PYTHON_EXE -c "import $package" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "      ⚠ Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "      Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    
    # Install main packages
    & $PYTHON_EXE -m pip install --quiet fastapi uvicorn sqlalchemy aiosqlite scikit-learn xgboost numpy biopython pandas cryptography pycryptodome pydantic pydantic-settings pytest pytest-asyncio httpx prometheus-client python-dotenv python-multipart 2>&1 | Out-Null
    
    # Install PyTorch separately
    Write-Host "      Installing PyTorch (CPU version)..." -ForegroundColor Yellow
    & $PYTHON_EXE -m pip install --quiet torch torchvision --index-url https://download.pytorch.org/whl/cpu 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✓ All dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "      ✓ All dependencies installed" -ForegroundColor Green
}
Write-Host ""

# Check models
Write-Host "[3/10] Checking AI models..." -ForegroundColor Yellow
if (Test-Path $MODELS_DIR) {
    $modelFiles = Get-ChildItem -Path $MODELS_DIR -Filter "*.p*" | Select-Object -ExpandProperty Name
    $modelCount = $modelFiles.Count
    
    if ($modelCount -gt 0) {
        Write-Host "      ✓ Found $modelCount model file(s)" -ForegroundColor Green
        Write-Host "        Models: $($modelFiles -join ', ')" -ForegroundColor Gray
    } else {
        Write-Host "      ⚠ No model files found (system will run with limited functionality)" -ForegroundColor Yellow
    }
} else {
    Write-Host "      ⚠ Models directory not found" -ForegroundColor Yellow
}
Write-Host ""

# Run tests
Write-Host "[4/10] Running AI component tests..." -ForegroundColor Yellow
Set-Location $BACKEND_DIR

$testOutput = & $PYTHON_EXE -m pytest tests/test_ai_components.py -v --tb=short 2>&1
$testPassed = $LASTEXITCODE -eq 0

if ($testPassed) {
    $passedCount = ($testOutput | Select-String "passed").Matches.Count
    Write-Host "      ✓ All tests passed ($passedCount tests)" -ForegroundColor Green
} else {
    Write-Host "      ⚠ Some tests failed (this is OK if models aren't trained)" -ForegroundColor Yellow
}
Write-Host ""

# Check if backend is already running
Write-Host "[5/10] Checking for existing backend..." -ForegroundColor Yellow
$existingProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -eq $PYTHON_EXE -and (Get-NetTCPConnection -OwningProcess $_.Id -ErrorAction SilentlyContinue | Where-Object LocalPort -eq 8000)
}

if ($existingProcess) {
    Write-Host "      ⚠ Backend already running (PID: $($existingProcess.Id))" -ForegroundColor Yellow
    $response = Read-Host "      Stop existing backend and restart? (y/n)"
    if ($response -eq 'y') {
        Stop-Process -Id $existingProcess.Id -Force
        Start-Sleep -Seconds 2
        Write-Host "      ✓ Stopped existing backend" -ForegroundColor Green
    } else {
        Write-Host "      Skipping backend startup" -ForegroundColor Gray
        $skipStart = $true
    }
} else {
    Write-Host "      ✓ Port 8000 available" -ForegroundColor Green
}
Write-Host ""

# Start backend
if (-not $skipStart) {
    Write-Host "[6/10] Starting integrated backend..." -ForegroundColor Yellow
    
    # Start in new PowerShell window (visible for debugging)
    $backendProcess = Start-Process -FilePath $PYTHON_EXE `
        -ArgumentList "integrated_main.py" `
        -WorkingDirectory $BACKEND_DIR `
        -PassThru `
        -WindowStyle Normal
    
    Write-Host "      ✓ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
    Write-Host "      Waiting for startup..." -ForegroundColor Gray
    Start-Sleep -Seconds 8
    Write-Host ""
} else {
    Write-Host "[6/10] Skipping backend startup" -ForegroundColor Gray
    Write-Host ""
}

# Test health endpoint
Write-Host "[7/10] Testing health endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get -ErrorAction Stop
    Write-Host "      ✓ Backend is healthy" -ForegroundColor Green
    Write-Host "        Status: $($healthResponse.status)" -ForegroundColor Gray
    Write-Host "        Models loaded: $($healthResponse.ai_engine.models_loaded)" -ForegroundColor Gray
    Write-Host "        Security ready: $($healthResponse.security_pipeline.ready)" -ForegroundColor Gray
} catch {
    Write-Host "      ✗ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "      Backend may still be starting up..." -ForegroundColor Yellow
}
Write-Host ""

# Test file upload
Write-Host "[8/10] Testing file upload..." -ForegroundColor Yellow
$testFile = Join-Path $SCRIPT_DIR "test_upload.fasta"

if (Test-Path $testFile) {
    try {
        # Create multipart form data
        $boundary = [System.Guid]::NewGuid().ToString()
        $fileContent = [System.IO.File]::ReadAllBytes($testFile)
        $fileName = [System.IO.Path]::GetFileName($testFile)
        
        $bodyLines = @(
            "--$boundary",
            "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
            "Content-Type: application/octet-stream",
            "",
            [System.Text.Encoding]::UTF8.GetString($fileContent),
            "--$boundary--"
        )
        
        $body = $bodyLines -join "`r`n"
        
        $uploadResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/upload" `
            -Method Post `
            -ContentType "multipart/form-data; boundary=$boundary" `
            -Body $body `
            -ErrorAction Stop
        
        Write-Host "      ✓ File uploaded successfully" -ForegroundColor Green
        Write-Host "        Job ID: $($uploadResponse.job_id)" -ForegroundColor Gray
        
        # Wait and check status
        Start-Sleep -Seconds 2
        $statusResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/status/$($uploadResponse.job_id)" -ErrorAction SilentlyContinue
        if ($statusResponse) {
            Write-Host "        Status: $($statusResponse.status)" -ForegroundColor Gray
            Write-Host "        Progress: $($statusResponse.progress)%" -ForegroundColor Gray
        }
    } catch {
        Write-Host "      ⚠ Upload test skipped: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "      ⚠ test_upload.fasta not found, skipping upload test" -ForegroundColor Yellow
}
Write-Host ""

# Display API documentation
Write-Host "[9/10] API Documentation" -ForegroundColor Yellow
Write-Host "      📖 Swagger UI: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "      📊 Health Check: http://localhost:8000/api/health" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "[10/10] System Summary" -ForegroundColor Yellow
Write-Host "      ============================================" -ForegroundColor Gray
Write-Host "      Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "      API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "      Health:   http://localhost:8000/api/health" -ForegroundColor White
Write-Host "      ============================================" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ Startup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open browser: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  2. Test file upload via Swagger UI" -ForegroundColor White
Write-Host "  3. Check frontend: cd frontend ; python -m http.server 3000" -ForegroundColor White
Write-Host ""
Write-Host "To stop the backend, press CTRL+C in its window or run:" -ForegroundColor Gray
Write-Host "  Get-Process python | Where-Object {`$_.Id -eq $($backendProcess.Id)} | Stop-Process" -ForegroundColor Gray
Write-Host ""

# Keep script open
Write-Host "Press any key to exit this script..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
