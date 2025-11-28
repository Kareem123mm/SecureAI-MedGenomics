"""Database initialization and models"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
import logging

from core.config import settings

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


# Database Models
class Job(Base):
    """Job processing model"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    filename = Column(String)
    file_size = Column(Integer)
    status = Column(String)  # queued, processing, completed, failed
    user_email = Column(String, nullable=True)
    encrypted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    security_score = Column(Float, default=100.0)
    aml_detected = Column(Boolean, default=False)
    ids_alerts = Column(Integer, default=0)


class SecurityEvent(Base):
    """Security event logging"""
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    event_type = Column(String)  # aml_detection, intrusion, encryption, etc.
    severity = Column(String)  # low, medium, high, critical
    description = Column(Text)
    job_id = Column(String, nullable=True)
    source_ip = Column(String, nullable=True)
    blocked = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


async def init_db():
    """Initialize database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_db():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
