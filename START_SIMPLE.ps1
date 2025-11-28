# ============================================
# SecureAI-MedGenomics - Simple Startup Script
# ============================================

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  SecureAI-MedGenomics Platform v2.0" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Find Python
$PYTHON_EXE = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe"

if (-not (Test-Path $PYTHON_EXE)) {
    Write-Host "✗ Python not found at: $PYTHON_EXE" -ForegroundColor Red
    Write-Host "Please update the script with your Python path" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Python: $PYTHON_EXE" -ForegroundColor Green

# Navigate to backend
$BACKEND_DIR = Join-Path $PSScriptRoot "backend"
Set-Location $BACKEND_DIR

Write-Host "✓ Backend directory: $BACKEND_DIR" -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "Running tests..." -ForegroundColor Yellow
& $PYTHON_EXE -m pytest tests/test_ai_components.py -v --tb=short
Write-Host ""

# Start backend
Write-Host "Starting backend..." -ForegroundColor Yellow
Write-Host "Backend will open in a new window" -ForegroundColor Gray
Write-Host ""

Start-Process -FilePath $PYTHON_EXE `
    -ArgumentList "integrated_main.py" `
    -WorkingDirectory $BACKEND_DIR `
    -WindowStyle Normal

Write-Host "✓ Backend starting..." -ForegroundColor Green
Write-Host "  Waiting 8 seconds for initialization..." -ForegroundColor Gray
Start-Sleep -Seconds 8

# Test health endpoint
Write-Host ""
Write-Host "Testing API..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health"
    Write-Host "✓ Backend is healthy!" -ForegroundColor Green
    Write-Host "  Models loaded: $($health.ai_engine.models_loaded)" -ForegroundColor Gray
    Write-Host "  Security ready: $($health.security_pipeline.ready)" -ForegroundColor Gray
} catch {
    Write-Host "⚠ Could not connect to backend yet" -ForegroundColor Yellow
    Write-Host "  It may still be starting up..." -ForegroundColor Gray
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  System Ready!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Health:   http://localhost:8000/api/health" -ForegroundColor White
Write-Host ""
Write-Host "To test upload, run: .\TEST_API.ps1" -ForegroundColor Cyan
Write-Host ""
