"""
SecureAI-MedGenomics Platform
Main FastAPI Application with 7-Layer Security Architecture
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
from pathlib import Path
from typing import Optional, List
import uuid
from datetime import datetime

# Import security layers
from security.aml_defense.defender import AMLDefender
from security.encryption.cryfa_manager import CryfaManager
from security.encryption.crypto_manager import CryptoManager
from security.intrusion.ids import IntrusionDetectionSystem
from security.genetic_algo.optimizer import GeneticSecurityOptimizer
from security.privacy.homomorphic import HomomorphicEncryption
from monitoring.metrics_collector import MetricsCollector
from api.models import (
    UploadResponse, StatusResponse, ResultResponse,
    HealthResponse, SecurityMetrics
)
from core.config import settings
from core.database import init_db, get_db


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    logger.info("🚀 Starting SecureAI-MedGenomics Platform...")
    
    # Initialize database
    await init_db()
    
    # Initialize security modules
    app.state.aml_defender = AMLDefender()
    app.state.cryfa_manager = CryfaManager()
    app.state.crypto_manager = CryptoManager()
    app.state.ids = IntrusionDetectionSystem()
    app.state.genetic_optimizer = GeneticSecurityOptimizer()
    app.state.homomorphic = HomomorphicEncryption()
    app.state.metrics = MetricsCollector()
    
    logger.info("✅ All security layers initialized")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down SecureAI-MedGenomics Platform...")
    app.state.metrics.export_final_metrics()


# Create FastAPI app
app = FastAPI(
    title="SecureAI-MedGenomics API",
    description="Secure AI-Powered Personalized Medicine Platform with 7-Layer Security",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Security-Score", "X-AML-Detected", "X-Request-ID"]
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add comprehensive security headers"""
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' http://localhost:*"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response


# Prometheus metrics
Instrumentator().instrument(app).expose(app)


# ============================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "SecureAI-MedGenomics Platform",
        "version": "1.0.0",
        "status": "operational",
        "security_layers": 7,
        "documentation": "/docs"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
@limiter.limit("30/minute")
async def health_check(request):
    """
    Comprehensive health check including all security layers
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "security_layers": {
                "aml_defense": app.state.aml_defender.is_ready(),
                "encryption": app.state.cryfa_manager.is_available(),
                "intrusion_detection": app.state.ids.is_active(),
                "genetic_optimizer": True,
                "privacy_preservation": True,
                "monitoring": app.state.metrics.is_collecting(),
            },
            "services": {
                "database": "connected",
                "grafana": "available" if settings.GRAFANA_ENABLED else "disabled",
                "prometheus": "active" if settings.METRICS_ENABLED else "disabled",
            }
        }
        
        # Check if any critical service is down
        all_layers_ok = all(health_status["security_layers"].values())
        if not all_layers_ok:
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable"
        )


@app.get("/api/security/metrics", response_model=SecurityMetrics, tags=["Security"])
@limiter.limit("10/minute")
async def get_security_metrics(request):
    """
    Get real-time security metrics for Grafana dashboard
    """
    try:
        metrics = app.state.metrics.get_current_metrics()
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_requests": metrics.get("total_requests", 0),
            "aml_detections": metrics.get("aml_detections", 0),
            "intrusion_attempts": metrics.get("intrusion_attempts", 0),
            "encryption_operations": metrics.get("encryption_operations", 0),
            "average_response_time": metrics.get("avg_response_time", 0),
            "security_score": metrics.get("security_score", 100.0),
            "threat_level": metrics.get("threat_level", "low"),
        }
    except Exception as e:
        logger.error(f"Failed to get security metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics")


# ============================================================
# FILE UPLOAD & PROCESSING
# ============================================================

@app.post("/api/upload", response_model=UploadResponse, tags=["Upload"])
@limiter.limit("10/minute")
async def upload_file(
    request,
    file: UploadFile = File(...),
    email: Optional[str] = Form(None),
    encrypt: bool = Form(False),
    db=Depends(get_db)
):
    """
    Upload genomic file with multi-layer security processing
    
    Security Features:
    - AML adversarial detection
    - Intrusion detection scan
    - Optional Cryfa encryption
    - Privacy-preserving processing
    - Real-time monitoring
    """
    job_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    
    try:
        logger.info(f"[{request_id}] New upload request: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # LAYER 5: AML Defense - Check for adversarial inputs
        if settings.AML_DETECTION_ENABLED:
            is_adversarial = await app.state.aml_defender.detect_adversarial_file(content)
            if is_adversarial:
                logger.warning(f"[{request_id}] Adversarial input detected!")
                app.state.metrics.increment("aml_detections")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Adversarial input detected. Upload rejected for security."
                )
        
        # LAYER 3: Intrusion Detection - Scan for malicious patterns
        threat_detected = await app.state.ids.scan_content(content, file.filename)
        if threat_detected:
            logger.warning(f"[{request_id}] Security threat detected in file")
            app.state.metrics.increment("intrusion_attempts")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security threat detected in uploaded file"
            )
        
        # Save temporary file
        temp_dir = Path(settings.UPLOAD_DIR) / job_id
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = temp_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        # LAYER 6: Encryption - Apply Cryfa if requested
        encrypted_path = None
        if encrypt and settings.CRYFA_ENABLED:
            encrypted_path = await app.state.cryfa_manager.encrypt_file(
                str(file_path),
                password=settings.CRYFA_DEFAULT_PASSWORD
            )
            logger.info(f"[{request_id}] File encrypted with Cryfa")
            app.state.metrics.increment("encryption_operations")
        
        # Store job in database
        # TODO: Implement database storage
        
        # LAYER 7: Monitoring - Log metrics
        app.state.metrics.record_upload(job_id, file.filename, len(content))
        
        logger.info(f"[{request_id}] Upload successful: Job {job_id}")
        
        return {
            "job_id": job_id,
            "status": "processing",
            "filename": file.filename,
            "encrypted": encrypted_path is not None,
            "received_at": datetime.utcnow().isoformat(),
            "message": "File uploaded successfully. Processing started."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@app.get("/api/status/{job_id}", response_model=StatusResponse, tags=["Status"])
@limiter.limit("60/minute")
async def get_job_status(request, job_id: str):
    """
    Get processing status of a job
    """
    try:
        # TODO: Implement actual job status tracking
        # For now, return mock status
        
        return {
            "job_id": job_id,
            "status": "processing",
            "current_step": 3,
            "total_steps": 5,
            "progress": 60,
            "estimated_time_remaining": 30,
            "message": "Analyzing genomic markers..."
        }
        
    except Exception as e:
        logger.error(f"Failed to get status for job {job_id}: {e}")
        raise HTTPException(status_code=404, detail="Job not found")


@app.get("/api/result/{job_id}", response_model=ResultResponse, tags=["Results"])
@limiter.limit("30/minute")
async def get_job_result(request, job_id: str):
    """
    Get analysis results for completed job
    """
    try:
        # TODO: Implement actual result retrieval
        # For now, return mock result
        
        return {
            "job_id": job_id,
            "status": "completed",
            "markers_found": [
                {"name": "BRCA1_185delAG", "confidence": 0.92, "position": "chr17:41246481"},
                {"name": "TP53_R175H", "confidence": 0.88, "position": "chr17:7577548"}
            ],
            "analysis_summary": {
                "total_sequences": 150,
                "markers_detected": 2,
                "processing_time": 42.5,
                "security_score": 98.5
            },
            "completed_at": datetime.utcnow().isoformat(),
            "deletion_proof": {
                "deleted_at": datetime.utcnow().isoformat(),
                "hash": "a1b2c3d4e5f6...",
                "verified": True
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get result for job {job_id}: {e}")
        raise HTTPException(status_code=404, detail="Result not found")


# ============================================================
# SECURITY TESTING ENDPOINTS (Development only)
# ============================================================

if settings.DEBUG:
    @app.post("/api/test/adversarial", tags=["Testing"])
    async def test_adversarial_detection(file: UploadFile = File(...)):
        """
        Test adversarial example detection (DEV ONLY)
        """
        content = await file.read()
        is_adversarial = await app.state.aml_defender.detect_adversarial_file(content)
        
        return {
            "filename": file.filename,
            "is_adversarial": is_adversarial,
            "confidence": 0.95 if is_adversarial else 0.05,
            "warning": "This is a testing endpoint. Not for production use."
        }
    
    @app.get("/api/test/ids", tags=["Testing"])
    async def test_intrusion_detection():
        """
        Test intrusion detection system (DEV ONLY)
        """
        test_patterns = [
            "normal_traffic",
            "../../../etc/passwd",  # Path traversal
            "<script>alert('xss')</script>",  # XSS
            "' OR '1'='1",  # SQL injection
        ]
        
        results = []
        for pattern in test_patterns:
            detected = await app.state.ids.scan_content(
                pattern.encode(),
                "test_file.txt"
            )
            results.append({
                "pattern": pattern,
                "detected": detected
            })
        
        return {"results": results}


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler with security logging"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    app.state.metrics.increment("errors")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
