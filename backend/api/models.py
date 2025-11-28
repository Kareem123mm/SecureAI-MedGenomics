"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    """Job processing status"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ThreatLevel(str, Enum):
    """Security threat level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================
# UPLOAD & PROCESSING
# ============================================================

class UploadResponse(BaseModel):
    """Response for file upload"""
    job_id: str
    status: str
    filename: str
    encrypted: bool
    received_at: str
    message: str


class StatusResponse(BaseModel):
    """Job status response"""
    job_id: str
    status: JobStatus
    current_step: int
    total_steps: int
    progress: float
    estimated_time_remaining: Optional[int] = None
    message: str


class Marker(BaseModel):
    """Genomic marker model"""
    name: str
    confidence: float
    position: Optional[str] = None
    description: Optional[str] = None


class AnalysisSummary(BaseModel):
    """Analysis summary"""
    total_sequences: int
    markers_detected: int
    processing_time: float
    security_score: float


class DeletionProof(BaseModel):
    """Proof of data deletion"""
    deleted_at: str
    hash: str
    verified: bool


class ResultResponse(BaseModel):
    """Analysis result response"""
    job_id: str
    status: JobStatus
    markers_found: List[Marker]
    analysis_summary: AnalysisSummary
    completed_at: str
    deletion_proof: DeletionProof


# ============================================================
# HEALTH & SECURITY
# ============================================================

class SecurityLayerStatus(BaseModel):
    """Status of individual security layer"""
    aml_defense: bool
    encryption: bool
    intrusion_detection: bool
    genetic_optimizer: bool
    privacy_preservation: bool
    monitoring: bool


class ServiceStatus(BaseModel):
    """Status of backend services"""
    database: str
    grafana: str
    prometheus: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    security_layers: SecurityLayerStatus
    services: ServiceStatus


class SecurityMetrics(BaseModel):
    """Real-time security metrics"""
    timestamp: str
    total_requests: int
    aml_detections: int
    intrusion_attempts: int
    encryption_operations: int
    average_response_time: float
    security_score: float
    threat_level: ThreatLevel


# ============================================================
# AML DEFENSE
# ============================================================

class AMLDetectionResult(BaseModel):
    """Result of adversarial ML detection"""
    is_adversarial: bool
    confidence: float
    perturbation_score: float
    detected_techniques: List[str]
    recommendation: str


class AMLDefenseConfig(BaseModel):
    """AML defense configuration"""
    enabled: bool
    threshold: float
    detection_methods: List[str]
    sanitization_enabled: bool


# ============================================================
# ENCRYPTION
# ============================================================

class EncryptionRequest(BaseModel):
    """Request for file encryption"""
    file_path: str
    password: str
    algorithm: str = "cryfa"


class EncryptionResponse(BaseModel):
    """Response for encryption operation"""
    success: bool
    encrypted_file_path: str
    compression_ratio: float
    encryption_time: float
    algorithm: str


# ============================================================
# INTRUSION DETECTION
# ============================================================

class IntrusionAlert(BaseModel):
    """Intrusion detection alert"""
    alert_id: str
    timestamp: str
    severity: ThreatLevel
    source_ip: str
    attack_type: str
    description: str
    blocked: bool


class IDSStats(BaseModel):
    """IDS statistics"""
    total_scans: int
    threats_detected: int
    threats_blocked: int
    false_positives: int
    detection_accuracy: float


# ============================================================
# GENETIC ALGORITHM
# ============================================================

class GAOptimizationResult(BaseModel):
    """Genetic algorithm optimization result"""
    generation: int
    best_fitness: float
    best_parameters: Dict[str, Any]
    evolution_history: List[float]
    convergence_achieved: bool


# ============================================================
# ADMIN
# ============================================================

class AdminLoginRequest(BaseModel):
    """Admin login request"""
    username: str
    password: str


class AdminToken(BaseModel):
    """Admin authentication token"""
    access_token: str
    token_type: str
    expires_in: int


class JobListItem(BaseModel):
    """Job list item for admin dashboard"""
    job_id: str
    filename: str
    status: JobStatus
    created_at: str
    completed_at: Optional[str] = None
    user_email: Optional[str] = None
    security_score: float


class SystemStats(BaseModel):
    """System statistics for admin"""
    total_jobs: int
    active_jobs: int
    completed_jobs: int
    failed_jobs: int
    total_uploads_size: int
    average_processing_time: float
    security_incidents: int
    uptime_seconds: int
