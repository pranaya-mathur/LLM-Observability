"""SQLAlchemy models for database persistence."""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Boolean,
    JSON,
)

from persistence.database import Base


class DetectionLog(Base):
    """Model for logging detection events."""
    
    __tablename__ = "detection_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Request info
    llm_response = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)
    
    # Detection results
    action = Column(String(20), nullable=False, index=True)  # allow, warn, block, log
    tier_used = Column(Integer, nullable=False, index=True)  # 1, 2, or 3
    method = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    processing_time_ms = Column(Float, nullable=False)
    
    # Failure info (if detected)
    failure_class = Column(String(100), nullable=True, index=True)
    severity = Column(String(20), nullable=True, index=True)
    explanation = Column(Text, nullable=False)
    blocked = Column(Boolean, nullable=False, default=False, index=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    request_id = Column(String(50), nullable=True, index=True)
    
    def __repr__(self) -> str:
        return (
            f"<DetectionLog(id={self.id}, tier={self.tier_used}, "
            f"action={self.action}, blocked={self.blocked})>"
        )


class SystemMetrics(Base):
    """Model for system-level metrics snapshots."""
    
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Tier distribution
    total_detections = Column(Integer, nullable=False)
    tier1_count = Column(Integer, nullable=False)
    tier2_count = Column(Integer, nullable=False)
    tier3_count = Column(Integer, nullable=False)
    
    tier1_pct = Column(Float, nullable=False)
    tier2_pct = Column(Float, nullable=False)
    tier3_pct = Column(Float, nullable=False)
    
    # Health
    is_healthy = Column(Boolean, nullable=False)
    health_message = Column(String(200), nullable=False)
    
    # Timestamp
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return (
            f"<SystemMetrics(id={self.id}, total={self.total_detections}, "
            f"healthy={self.is_healthy})>"
        )
