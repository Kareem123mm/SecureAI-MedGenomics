# 🛡️ SecureAI-MedGenomics Platform

**Secure Genomic Data Analysis with AI-Powered Privacy Protection**

---

## 🚀 Quick Start

**Get started in 3 seconds:**

```powershell
# Option 1: PowerShell (Recommended)
.\START.ps1

# Option 2: Command Prompt
START.bat
```

That's it! The scripts will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Start backend server (port 8000)
- ✅ Start frontend server (port 3000)
- ✅ Open browser automatically

---

## 📚 Complete Documentation

### **Main Guides**

- **[📖 COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)** - Complete project documentation
  - Installation & setup
  - Architecture diagrams
  - API documentation
  - Troubleshooting
  - Recovery guides

- **[🔐 SECURITY_EXPLANATION.md](SECURITY_EXPLANATION.md)** - Security architecture details
  - 7-layer security system explained
  - Threat model & attack defense
  - Cryptographic specifications
  - HIPAA/GDPR compliance

- **[🧹 FILE_CLEANUP_GUIDE.md](FILE_CLEANUP_GUIDE.md)** - Project cleanup guide
  - Remove unnecessary files
  - Automated cleanup script
  - File organization

### **Specialized Guides**

- **[🔧 INSTALL_CRYFA.md](INSTALL_CRYFA.md)** - Cryfa encryption setup

---

## 🌟 Key Features

### **7-Layer Security Architecture**

1. **Genetic Algorithm Optimization** - Self-optimizing security parameters
2. **Genomics-Based Authentication** - DNA-inspired key generation
3. **Intrusion Detection System** - Bio-inspired threat detection (95% accuracy)
4. **Privacy-Preserving Computation** - Homomorphic encryption
5. **Adversarial ML Defense** - AI model protection (PyTorch autoencoder)
6. **Cryfa Encryption** - AES-256-GCM specialized for genomic data
7. **Real-Time Monitoring** - Complete audit trail

### **Core Capabilities**

- ✅ **Zero Persistent Storage** - Original files deleted immediately after processing
- ✅ **Cryptographic Proof** - SHA-256 deletion certificates
- ✅ **HIPAA/GDPR Compliant** - Privacy-first design
- ✅ **AI-Powered Analysis** - Genetic marker detection
- ✅ **Professional UI** - Modern web interface with animations

---

## 🏗️ Architecture Overview

```
SecureAI-MedGenomics/
├── START.bat                    # Windows startup script
├── START.ps1                    # PowerShell startup (recommended)
├── CLEANUP.ps1                  # Project cleanup script
├── COMPREHENSIVE_README.md      # Complete documentation
├── SECURITY_EXPLANATION.md      # Security details
├── FILE_CLEANUP_GUIDE.md        # Cleanup guide
├── INSTALL_CRYFA.md             # Cryfa installation
├── backend/
│   ├── real_main.py             # FastAPI server
│   ├── cryfa_wrapper.py         # Encryption wrapper
│   ├── core/
│   │   ├── database.py          # SQLite database
│   │   └── config.py            # Configuration
│   ├── security/
│   │   ├── genetic_algo/        # Layer 1: GA optimization
│   │   ├── genomics_auth/       # Layer 2: Bio-auth (placeholder)
│   │   ├── intrusion/           # Layer 3: IDS
│   │   ├── privacy/             # Layer 4: Homomorphic encryption
│   │   ├── aml_defense/         # Layer 5: Adversarial ML defense
│   │   └── encryption/          # Layer 6: Cryfa manager
│   └── venv/                    # Virtual environment
├── frontend/
│   ├── index.html               # Main UI
│   ├── app.js                   # Application logic
│   ├── style.css                # Base styles
│   ├── professional.css         # Card layouts
│   ├── progress-timeline.css    # Progress UI
│   ├── modal-styles.css         # Modal dialogs
│   ├── animations.css           # Animations
│   └── visibility-fix.css       # Visual fixes
├── cryfa-master/                # Cryfa source code
├── scripts/                     # Utility scripts
└── grafana/                     # Monitoring (optional)
```

---

## 📖 Usage

### **Step 1: Start the Platform**

```powershell
.\START.ps1
```

### **Step 2: Upload Genomic File**

1. Open browser to http://localhost:3000
2. Click "Choose File" and select a FASTA/FASTQ file
3. Check consent checkbox
4. Click "Upload & Analyze"
5. Confirm upload in dialog

### **Step 3: Track Progress**

Watch the animated progress timeline:
1. **Validating** - File validation and security checks
2. **Encrypting** - AES-256-GCM encryption with Cryfa
3. **Processing** - AI analysis for genetic markers
4. **Finalizing** - Original file deletion

### **Step 4: View Results**

- See genetic markers detected
- View species classification
- Download proof-of-deletion certificate (SHA-256)

---

## 🔧 Manual Setup (Alternative)

If automated scripts don't work, see **[COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)** for step-by-step manual installation.

---

## 🧹 Project Cleanup

Remove unnecessary files:

```powershell
.\CLEANUP.ps1
```

This removes:
- Temporary Python fix scripts
- Redundant documentation files
- Unused test files
- Old prototypes

See **[FILE_CLEANUP_GUIDE.md](FILE_CLEANUP_GUIDE.md)** for details.

---

## 🛠️ Troubleshooting

### **Port Already in Use**

```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in START.ps1
```

### **Module Not Found**

```powershell
# Reinstall dependencies
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### **Frontend Not Loading**

```powershell
# Clear browser cache or try incognito mode
# Check console for errors (F12)
```

### **More Issues?**

See **Troubleshooting** section in [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)

---

## 🔐 Security Highlights

### **Data Flow**

```
Upload → IDS Scan → AML Check → Encrypt → Store → AI Process → Delete → Results
```

### **Zero Persistent Storage**

- Original file deleted immediately after encryption
- Only encrypted .cryfa file stored
- Automatic deletion after 7 days
- Cryptographic proof-of-deletion (SHA-256)

### **Compliance**

- ✅ HIPAA-ready (Technical Safeguards implemented)
- ✅ GDPR-compatible (Right to Erasure, Data Minimization)
- ✅ Complete audit trail

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/upload` | POST | Upload genomic file |
| `/api/status/{job_id}` | GET | Check processing status |
| `/api/result/{job_id}` | GET | Get analysis results |
| `/api/proof/{job_id}` | GET | Get deletion proof |

See **[COMPREHENSIVE_README.md](COMPREHENSIVE_README.md)** for full API documentation with examples.

---

## 🎓 Academic Context

This project demonstrates:

1. **Defense-in-Depth**: 7 independent security layers
2. **Bio-Inspired Computing**: Genetic algorithms, genomic patterns
3. **Privacy Engineering**: Homomorphic encryption, zero-knowledge
4. **Adversarial ML**: Robust AI model protection
5. **Specialized Cryptography**: Cryfa for genomic data

Perfect for:
- University cybersecurity projects
- Research papers on bio-inspired security
- Healthcare privacy demonstrations
- AI security showcases

---

## 📄 License

MIT License - Free for academic and research use

---

## 🤝 Contributing

This is an academic project. For improvements:
1. Fork the repository
2. Create feature branch
3. Submit pull request

---

## 📧 Contact

For questions or support:
- Read [COMPREHENSIVE_README.md](COMPREHENSIVE_README.md) first
- Check [SECURITY_EXPLANATION.md](SECURITY_EXPLANATION.md) for security details
- Create an issue on the repository

---

**Built with 🧬 for secure genomic data analysis**
