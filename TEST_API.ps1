# Quick Test Script for SecureAI-MedGenomics Backend
# Tests all API endpoints

Write-Host "🧪 Testing SecureAI-MedGenomics API..." -ForegroundColor Cyan
Write-Host ""

$BASE_URL = "http://localhost:8000"

# Test 1: Health Check
Write-Host "[1/4] Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BASE_URL/api/health" -Method Get
    Write-Host "  ✓ Status: $($health.status)" -ForegroundColor Green
    Write-Host "  ✓ Models loaded: $($health.ai_engine.models_loaded)" -ForegroundColor Green
    Write-Host "  ✓ Security ready: $($health.security_pipeline.ready)" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: System Stats
Write-Host "[2/4] Testing System Stats..." -ForegroundColor Yellow
try {
    $stats = Invoke-RestMethod -Uri "$BASE_URL/api/system/stats" -Method Get -ErrorAction SilentlyContinue
    if ($stats) {
        Write-Host "  ✓ System stats retrieved" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Endpoint not available" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Endpoint not available" -ForegroundColor Yellow
}
Write-Host ""

# Test 3: File Upload
Write-Host "[3/4] Testing File Upload..." -ForegroundColor Yellow
$testFile = Join-Path (Split-Path -Parent $PSCommandPath) "test_upload.fasta"

if (-not (Test-Path $testFile)) {
    # Create a test file
    Write-Host "  Creating test FASTA file..." -ForegroundColor Gray
    $testContent = @"
>test_sequence_1
ATCGATCGATCGATCGATCGATCGATCGATCG
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA
>test_sequence_2
TTTTAAAACCCCGGGGTTTTAAAACCCCGGGG
ATATATATATCGCGCGCGTGTGTGTGCACACA
"@
    Set-Content -Path $testFile -Value $testContent
}

try {
    # Use Invoke-WebRequest for multipart form data
    $form = @{
        file = Get-Item -Path $testFile
    }
    
    $upload = Invoke-RestMethod -Uri "$BASE_URL/api/upload" -Method Post -Form $form
    
    Write-Host "  ✓ Upload successful" -ForegroundColor Green
    Write-Host "  ✓ Job ID: $($upload.job_id)" -ForegroundColor Green
    
    $jobId = $upload.job_id
    
    # Test 4: Check Status
    Write-Host ""
    Write-Host "[4/4] Testing Status Endpoint..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    try {
        $status = Invoke-RestMethod -Uri "$BASE_URL/api/status/$jobId" -Method Get
        Write-Host "  ✓ Status: $($status.status)" -ForegroundColor Green
        Write-Host "  ✓ Progress: $($status.progress)%" -ForegroundColor Green
        Write-Host "  ✓ Current stage: $($status.current_stage)" -ForegroundColor Green
        
        # Wait for completion
        if ($status.status -eq "processing") {
            Write-Host ""
            Write-Host "  Waiting for processing to complete..." -ForegroundColor Gray
            
            $maxWait = 30
            $waited = 0
            while ($waited -lt $maxWait) {
                Start-Sleep -Seconds 2
                $waited += 2
                
                $status = Invoke-RestMethod -Uri "$BASE_URL/api/status/$jobId" -Method Get
                Write-Host "  Progress: $($status.progress)% - $($status.current_stage)" -ForegroundColor Gray
                
                if ($status.status -eq "completed") {
                    Write-Host ""
                    Write-Host "  ✓ Processing completed!" -ForegroundColor Green
                    
                    # Get results
                    try {
                        $results = Invoke-RestMethod -Uri "$BASE_URL/api/result/$jobId" -Method Get
                        Write-Host ""
                        Write-Host "  Results:" -ForegroundColor Cyan
                        Write-Host "    Security Score: $($results.security_report.security_score)" -ForegroundColor White
                        if ($results.ai_analysis.disease_risk) {
                            Write-Host "    Disease Risk: $($results.ai_analysis.disease_risk.risk_probability)" -ForegroundColor White
                        }
                        if ($results.ai_analysis.drug_response) {
                            Write-Host "    Drug Response: $($results.ai_analysis.drug_response.response_value)" -ForegroundColor White
                        }
                    } catch {
                        Write-Host "  ⚠ Could not retrieve results" -ForegroundColor Yellow
                    }
                    break
                }
                
                if ($status.status -eq "failed") {
                    Write-Host "  ✗ Processing failed" -ForegroundColor Red
                    break
                }
            }
            
            if ($waited -ge $maxWait) {
                Write-Host "  ⚠ Timeout waiting for completion" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "  ✗ Status check failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "  ✗ Upload failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Error details:" -ForegroundColor Gray
    Write-Host "  $($_.ErrorDetails.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ Testing complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📖 View full API docs: $BASE_URL/docs" -ForegroundColor Cyan
Write-Host ""
