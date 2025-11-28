# ============================================
# SecureAI-MedGenomics Integrated Backend
# PowerShell Startup Script
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SecureAI-MedGenomics Platform v2.0" -ForegroundColor Green
Write-Host "  Integrated Backend Startup" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Store the project root
$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$BACKEND_DIR = Join-Path $PROJECT_ROOT "backend"

# Navigate to backend directory
Set-Location $BACKEND_DIR

# Check Python version
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "      ✓ $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($matches) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
            Write-Host "      ✗ Python 3.9+ required!" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "      ✗ Python not found!" -ForegroundColor Red
    Write-Host "      Please install Python 3.9+ from https://python.org" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if requirements are installed
Write-Host "[2/6] Checking dependencies..." -ForegroundColor Yellow

$requiredPackages = @("fastapi", "torch", "sklearn", "xgboost", "uvicorn")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $installed = python -c "import $package" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "      ⚠ Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "      Installing dependencies..." -ForegroundColor Yellow
    
    pip install -r requirements_integrated.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "      ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "      ✓ All dependencies installed" -ForegroundColor Green
}

Write-Host ""

# Check if models directory exists
Write-Host "[3/6] Checking AI models..." -ForegroundColor Yellow
$MODELS_DIR = Join-Path $PROJECT_ROOT "models_export"

if (Test-Path $MODELS_DIR) {
    $modelFiles = @(
        "nn_disease_risk.pth",
        "rf_disease_risk.pkl",
        "xgb_disease_risk.pkl",
        "nn_drug_response.pth",
        "rf_drug_response.pkl",
        "xgb_drug_response.pkl"
    )
    
    $missingModels = @()
    foreach ($model in $modelFiles) {
        $modelPath = Join-Path $MODELS_DIR $model
        if (-not (Test-Path $modelPath)) {
            $missingModels += $model
        }
    }
    
    if ($missingModels.Count -eq 0) {
        Write-Host "      ✓ All 6 models found" -ForegroundColor Green
    } else {
        Write-Host "      ⚠ Missing models: $($missingModels -join ', ')" -ForegroundColor Yellow
        Write-Host "      System will run with available models" -ForegroundColor Yellow
    }
} else {
    Write-Host "      ✗ Models directory not found!" -ForegroundColor Red
    Write-Host "      Expected: $MODELS_DIR" -ForegroundColor Red
}

Write-Host ""

# Check if database directory exists
Write-Host "[4/6] Checking database..." -ForegroundColor Yellow
$DB_FILE = Join-Path $BACKEND_DIR "genomic_data.db"

if (Test-Path $DB_FILE) {
    Write-Host "      ✓ Database exists" -ForegroundColor Green
} else {
    Write-Host "      ⚠ Database will be created on first run" -ForegroundColor Yellow
}

Write-Host ""

# Check if security modules exist
Write-Host "[5/6] Checking security modules..." -ForegroundColor Yellow
$SECURITY_DIR = Join-Path $BACKEND_DIR "security"

if (Test-Path $SECURITY_DIR) {
    Write-Host "      ✓ Security modules found" -ForegroundColor Green
} else {
    Write-Host "      ✗ Security directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Final system check
Write-Host "[6/6] Running pre-flight checks..." -ForegroundColor Yellow

# Check if integrated_main.py exists
$MAIN_FILE = Join-Path $BACKEND_DIR "integrated_main.py"
if (-not (Test-Path $MAIN_FILE)) {
    Write-Host "      ✗ integrated_main.py not found!" -ForegroundColor Red
    Write-Host "      Expected: $MAIN_FILE" -ForegroundColor Red
    exit 1
}

Write-Host "      ✓ All checks passed" -ForegroundColor Green
Write-Host ""

# Display system info
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  System Configuration" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Health:   http://localhost:8000/api/health" -ForegroundColor White
Write-Host ""
Write-Host "  Working Directory: $BACKEND_DIR" -ForegroundColor Gray
Write-Host "  Models Directory:  $MODELS_DIR" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Ask user if they want to run tests first
Write-Host "Options:" -ForegroundColor Yellow
Write-Host "  [1] Start backend immediately" -ForegroundColor White
Write-Host "  [2] Run tests first, then start" -ForegroundColor White
Write-Host "  [3] Run tests only" -ForegroundColor White
Write-Host "  [4] Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Starting backend..." -ForegroundColor Green
        Write-Host ""
        python integrated_main.py
    }
    "2" {
        Write-Host ""
        Write-Host "🧪 Running tests..." -ForegroundColor Yellow
        Write-Host ""
        pytest tests/ -v
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ All tests passed!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🚀 Starting backend..." -ForegroundColor Green
            Write-Host ""
            python integrated_main.py
        } else {
            Write-Host ""
            Write-Host "❌ Tests failed! Fix errors before starting." -ForegroundColor Red
            exit 1
        }
    }
    "3" {
        Write-Host ""
        Write-Host "🧪 Running tests..." -ForegroundColor Yellow
        Write-Host ""
        pytest tests/ -v
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ All tests passed!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "❌ Some tests failed." -ForegroundColor Red
            exit 1
        }
    }
    "4" {
        Write-Host ""
        Write-Host "Exiting..." -ForegroundColor Gray
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}
