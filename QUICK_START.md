# 🚀 **QUICK START GUIDE**
## Get Running in 5 Minutes

---

## ⚡ **FASTEST WAY TO START**

### **1. Install Dependencies (One Time)**

```powershell
cd backend
pip install -r requirements_integrated.txt
```

### **2. Start the Integrated Backend**

```powershell
.\START_INTEGRATED.ps1
```

**OR manually:**

```powershell
cd backend
python integrated_main.py
```

### **3. Verify It's Working**

Open browser to: `http://localhost:8000/docs`

You should see the FastAPI documentation page.

---

## 🧪 **QUICK TEST**

### **Run All Tests:**

```powershell
cd backend
pytest tests/ -v
```

### **Test Individual Components:**

```powershell
# Test AI models
pytest tests/test_ai_components.py -v

# Test security
pytest tests/test_security_layers.py -v

# Test full pipeline
pytest tests/test_integration.py -v
```

---

## 📤 **UPLOAD A FILE**

### **Using cURL:**

```powershell
curl -X POST "http://localhost:8000/api/upload" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@test_upload.fasta"
```

### **Using PowerShell:**

```powershell
$file = Get-Item "test_upload.fasta"
$boundary = [System.Guid]::NewGuid().ToString()
$headers = @{
    "Content-Type" = "multipart/form-data; boundary=$boundary"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/upload" `
  -Method POST -InFile $file.FullName -Headers $headers
```

### **Using the Frontend:**

1. Start frontend:
```powershell
cd frontend
python -m http.server 3000
```

2. Open: `http://localhost:3000`
3. Click "Upload File" and select a FASTA file

---

## 🔍 **CHECK RESULTS**

### **Get Job Status:**

```powershell
curl http://localhost:8000/api/status/<JOB_ID>
```

### **Get Full Results:**

```powershell
curl http://localhost:8000/api/result/<JOB_ID>
```

---

## ✅ **WHAT TO EXPECT**

### **Health Check Response:**

```json
{
  "status": "healthy",
  "security_pipeline": {
    "ready": true,
    "security_score": 100.0
  },
  "ai_engine": {
    "ready": true,
    "models_loaded": 6
  }
}
```

### **Processing Time:**

- Small file (<1MB): **3-5 seconds**
- Medium file (1-10MB): **5-15 seconds**
- Large file (>10MB): **15-30 seconds**

### **AI Results Format:**

```json
{
  "disease_risk": {
    "risk_probability": 0.45,
    "risk_level": "medium",
    "confidence": 0.92
  },
  "drug_response": {
    "response_value": 0.68,
    "response_category": "good",
    "confidence": 0.88
  }
}
```

---

## 🐛 **TROUBLESHOOTING**

### **Port Already in Use:**

```powershell
# Kill process on port 8000
$process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
}

# Then restart
python integrated_main.py
```

### **Models Not Loading:**

```powershell
# Check models directory
ls models_export\

# Should see 6 .pth and .pkl files
# If missing, download from project repo
```

### **Import Errors:**

```powershell
# Make sure you're in backend directory
cd backend

# Set PYTHONPATH
$env:PYTHONPATH = "D:\university\Siminar and project\SecureAI-MedGenomics\backend"

# Run again
python integrated_main.py
```

---

## 📊 **SYSTEM REQUIREMENTS**

- **Python:** 3.9+
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 2GB for models and dependencies
- **OS:** Windows 10/11, Linux, macOS

---

## 🎯 **NEXT STEPS**

1. ✅ Start backend → **You're here!**
2. 📤 Upload test file
3. 🔍 Check results
4. 🧪 Run tests
5. 🎨 Customize frontend
6. 🚀 Deploy to production

---

## 📚 **MORE DOCUMENTATION**

- **Complete Guide:** `INTEGRATION_COMPLETE.md`
- **Architecture:** See processing pipeline in main docs
- **API Reference:** `http://localhost:8000/docs`
- **Security Details:** `SECURITY_LAYERS_DETAILED.md`

---

## 💡 **TIPS**

1. **Use the startup script** (`START_INTEGRATED.ps1`) - it checks everything
2. **Run tests first** to ensure everything works
3. **Check health endpoint** before uploading files
4. **Use small test files** first to verify pipeline
5. **Monitor console logs** for detailed progress

---

## ⚡ **ULTRA-QUICK COMMANDS**

```powershell
# Install → Test → Run (one command)
cd backend; pip install -r requirements_integrated.txt; pytest tests/ -v; python integrated_main.py

# Just run (if already installed)
cd backend; python integrated_main.py

# Run with auto-reload (development)
cd backend; uvicorn integrated_main:app --reload --host 0.0.0.0 --port 8000
```

---

**Ready to go!** 🎉

If you encounter issues, check `INTEGRATION_COMPLETE.md` for detailed troubleshooting.
