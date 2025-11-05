# 🔐 Installing Cryfa on Windows

**Cryfa** is the genomic encryption tool from https://github.com/cobilab/cryfa

Your backend is **already integrated** with Cryfa - you just need to install it!

---

## ✅ **Option 1: Download Pre-built Binary (EASIEST)**

### **Step 1: Download Cryfa**
```powershell
# Download the latest release from GitHub
# Go to: https://github.com/cobilab/cryfa/releases

# Or download directly:
Invoke-WebRequest -Uri "https://github.com/cobilab/cryfa/releases/download/v20.7/cryfa-windows.exe" -OutFile "cryfa.exe"
```

### **Step 2: Move to System Path**
```powershell
# Create a tools directory
New-Item -ItemType Directory -Force -Path "C:\Program Files\Cryfa"

# Move the executable
Move-Item -Path "cryfa.exe" -Destination "C:\Program Files\Cryfa\cryfa.exe"

# Add to PATH (requires admin)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Cryfa", "Machine")
```

### **Step 3: Verify Installation**
```powershell
# Restart PowerShell, then:
cryfa --version
```

---

## ✅ **Option 2: Build from Source (Advanced)**

### **Requirements:**
- CMake
- Visual Studio Build Tools
- Git

### **Step 1: Install Dependencies**
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install CMake and Git
choco install cmake git visualstudio2022-workload-vctools -y
```

### **Step 2: Clone and Build**
```powershell
# Clone the repository
cd "D:\university\Siminar and project"
git clone https://github.com/cobilab/cryfa.git
cd cryfa

# Build
cmake -B build -G "Visual Studio 17 2022"
cmake --build build --config Release

# Copy executable
Copy-Item "build\Release\cryfa.exe" -Destination "C:\Windows\System32\"
```

### **Step 3: Verify**
```powershell
cryfa --version
```

---

## ✅ **Option 3: Use WSL (Linux Subsystem)**

### **Step 1: Enable WSL**
```powershell
wsl --install
```

### **Step 2: Install in WSL**
```bash
# Inside WSL Ubuntu
sudo apt-get update
sudo apt-get install -y cryfa

# Or build from source:
sudo apt-get install -y git cmake build-essential
git clone https://github.com/cobilab/cryfa.git
cd cryfa
cmake .
make
sudo make install
```

### **Step 3: Update Backend Config**
Edit `backend/core/config.py`:
```python
# For WSL
CRYFA_PATH = "wsl cryfa"
```

Then update `cryfa_manager.py`:
```python
self.cryfa_path = settings.CRYFA_PATH or "cryfa"
```

---

## 🧪 **Test Cryfa Integration**

After installation, test it:

```powershell
cd "D:\university\Siminar and project\SecureAI-MedGenomics\backend"
.\venv\Scripts\activate
python -c "from security.encryption.cryfa_manager import CryfaManager; m = CryfaManager(); print('✅ Cryfa available!' if m.is_available() else '❌ Not found')"
```

Or run the full test:
```powershell
python -m security.encryption.cryfa_manager
```

---

## 📊 **What Cryfa Does in Your Project**

1. **Genomic Compression**: 10-20x better than gzip for FASTA files
2. **AES-256 Encryption**: Military-grade security
3. **Format Preservation**: Maintains FASTA/FASTQ/VCF structure
4. **Fast**: Optimized for large genomic datasets

### **Usage in Your Backend:**

When a user uploads a file with encryption enabled:

```python
# Backend automatically calls:
encrypted_file = await cryfa_manager.encrypt_file(
    input_file="patient_genome.fasta",
    password="secure_password",
    verbose=True
)

# Creates: patient_genome.cryfa (compressed + encrypted)
```

---

## 🔧 **Troubleshooting**

### **"Cryfa not found"**
- Make sure `cryfa.exe` is in your PATH
- Try full path: `C:\Program Files\Cryfa\cryfa.exe`

### **"Permission denied"**
- Run PowerShell as Administrator
- Check file permissions on cryfa.exe

### **"CMake error" (building from source)**
- Install Visual Studio Build Tools
- Make sure CMake is in PATH

---

## 🚀 **Quick Install (Recommended for Demo)**

For your university project demo, use **Option 1**:

```powershell
# 1. Download
Invoke-WebRequest -Uri "https://github.com/cobilab/cryfa/releases/latest/download/cryfa.exe" -OutFile "cryfa.exe"

# 2. Move to project
Move-Item "cryfa.exe" -Destination "D:\university\Siminar and project\SecureAI-MedGenomics\cryfa.exe"

# 3. Update backend config
# Edit backend/core/config.py:
# CRYFA_PATH = r"D:\university\Siminar and project\SecureAI-MedGenomics\cryfa.exe"
```

Then restart your backend!

---

## ✅ **After Installation**

Your platform will automatically:
- ✅ Detect Cryfa is available
- ✅ Enable encryption option in API
- ✅ Compress genomic files 10-20x
- ✅ Apply AES-256 encryption
- ✅ Track metrics in Grafana

**Your security dashboard will show encryption stats! 📊**

---

**Need help? Check the Cryfa documentation:**
https://github.com/cobilab/cryfa

**Your integration is ready - just install Cryfa! 🚀**
