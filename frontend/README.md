# Integrated Secure Website

Your original website has been enhanced with SecureAI-MedGenomics security features!

## What's New?

### 🛡️ Security Enhancements
- **AML Defense**: All uploads protected against adversarial attacks
- **Cryfa Encryption**: Automatic genomic data encryption
- **Intrusion Detection**: Real-time threat scanning
- **Rate Limiting**: Protection against DoS attacks
- **Security Headers**: CSP, HSTS, X-Frame-Options

### 📊 Monitoring
- Real-time metrics in Grafana dashboard
- Security event logging
- Performance monitoring

## Running the Website

### Development Mode
```bash
# 1. Start the secure backend
cd ../backend
python -m uvicorn main:app --reload

# 2. Serve frontend (choose one)
# Option A: Simple HTTP server
python -m http.server 3000

# Option B: Live server (if installed)
npx live-server --port=3000

# Option C: VS Code Live Server extension
# Right-click index.html > "Open with Live Server"
```

### Access Points
- **Website**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001

## API Integration

The website now connects to the secure backend:

```javascript
// Example: Secure file upload
const formData = new FormData();
formData.append('file', file);
formData.append('encrypt', true);

const response = await fetch('http://localhost:8000/api/upload', {
    method: 'POST',
    body: formData
});
```

## Security Features in Action

### 1. AML Protection
Every upload is scanned for adversarial content before processing.

### 2. Encryption
Enable Cryfa encryption with one checkbox - automatic 10-20x compression!

### 3. Monitoring
View real-time security metrics in Grafana:
- Threat detections
- Upload statistics
- System performance
- Security score

## Troubleshooting

### Backend not connected
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# If not, start it
cd ../backend
uvicorn main:app --reload
```

### CORS errors
The backend is configured to allow requests from:
- http://localhost:3000
- http://localhost:5173
- http://localhost:8080

If you're using a different port, update `backend/core/config.py`:
```python
CORS_ORIGINS = [
    "http://localhost:YOUR_PORT",
    ...
]
```

## Next Steps

1. **Test Security Features**: Try uploading different file types
2. **Check Grafana**: Open http://localhost:3001 to see metrics
3. **Read Documentation**: See ../docs/ for detailed guides
4. **Team Collaboration**: Share API endpoints with AI/Data teams

---

**Built with ❤️ by SecureAI-MedGenomics**
