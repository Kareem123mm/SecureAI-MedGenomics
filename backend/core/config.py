"""
Configuration settings for SecureAI-MedGenomics Platform
"""

from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_USE_STRONG_RANDOM_KEY"
    JWT_SECRET_KEY: str = "CHANGE_THIS_JWT_KEY_IN_PRODUCTION"
    ENCRYPTION_KEY_PATH: str = "./secrets/encryption.key"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./secureai_medgenomics.db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]
    
    # File Upload
    UPLOAD_DIR: Path = Path("uploads")
    RESULTS_DIR: Path = Path("results")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = [".fasta", ".fa", ".vcf", ".txt"]
    
    # Cryfa Configuration
    CRYFA_ENABLED: bool = True
    CRYFA_DEFAULT_PASSWORD: str = "ChangeMe123!"
    CRYFA_KMER_SIZE: int = 21
    
    # AML Defense
    AML_DETECTION_ENABLED: bool = True
    AML_THRESHOLD: float = 0.85
    AML_MODEL_PATH: str = "./models/aml_detector.pth"
    
    # Intrusion Detection
    IDS_ENABLED: bool = True
    IDS_SENSITIVITY: str = "HIGH"  # LOW, MEDIUM, HIGH
    IDS_ALGORITHM: str = "BIOINSPIRED_SUFFIX_TREE"
    
    # Genetic Algorithm
    GA_POPULATION_SIZE: int = 50
    GA_GENERATIONS: int = 100
    GA_MUTATION_RATE: float = 0.1
    
    # Privacy & Encryption
    HOMOMORPHIC_ENABLED: bool = False  # Computationally expensive
    ENCRYPTION_ALGORITHM: str = "AES-256-GCM"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Monitoring
    GRAFANA_ENABLED: bool = True
    GRAFANA_URL: str = "http://localhost:3001"
    GRAFANA_API_KEY: str = ""
    PROMETHEUS_URL: str = "http://localhost:9090"
    METRICS_ENABLED: bool = True
    METRICS_INTERVAL: int = 10  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/secureai.log"
    
    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "genomics2025"  # CHANGE IN PRODUCTION
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Create necessary directories
settings.UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
settings.RESULTS_DIR.mkdir(exist_ok=True, parents=True)
Path("logs").mkdir(exist_ok=True)
Path("secrets").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)
