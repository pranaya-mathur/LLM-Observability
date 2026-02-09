"""Repository pattern for database operations."""

from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from persistence.models import DetectionLog, SystemMetrics


class DetectionRepository:
    """Repository for detection log operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, detection_data: dict) -> DetectionLog:
        """Create a new detection log entry.
        
        Args:
            detection_data: Dictionary with detection information
            
        Returns:
            Created DetectionLog instance
        """
        log = DetectionLog(**detection_data)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
    
    def get_by_id(self, log_id: int) -> Optional[DetectionLog]:
        """Get detection log by ID."""
        return self.db.query(DetectionLog).filter(DetectionLog.id == log_id).first()
    
    def get_recent(self, limit: int = 100) -> List[DetectionLog]:
        """Get recent detection logs."""
        return (
            self.db.query(DetectionLog)
            .order_by(desc(DetectionLog.created_at))
            .limit(limit)
            .all()
        )
    
    def get_by_tier(self, tier: int, limit: int = 100) -> List[DetectionLog]:
        """Get detection logs filtered by tier."""
        return (
            self.db.query(DetectionLog)
            .filter(DetectionLog.tier_used == tier)
            .order_by(desc(DetectionLog.created_at))
            .limit(limit)
            .all()
        )
    
    def get_blocked_count(self, hours: int = 24) -> int:
        """Get count of blocked detections in the last N hours."""
        since = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.db.query(func.count(DetectionLog.id))
            .filter(DetectionLog.blocked == True)
            .filter(DetectionLog.created_at >= since)
            .scalar()
        )
    
    def get_tier_distribution(self, hours: int = 24) -> dict:
        """Get tier distribution for the last N hours."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        total = (
            self.db.query(func.count(DetectionLog.id))
            .filter(DetectionLog.created_at >= since)
            .scalar()
        )
        
        if total == 0:
            return {"tier1": 0, "tier2": 0, "tier3": 0, "total": 0}
        
        tier_counts = (
            self.db.query(
                DetectionLog.tier_used,
                func.count(DetectionLog.id).label("count")
            )
            .filter(DetectionLog.created_at >= since)
            .group_by(DetectionLog.tier_used)
            .all()
        )
        
        distribution = {f"tier{t}": c for t, c in tier_counts}
        distribution["total"] = total
        
        return distribution


class MetricsRepository:
    """Repository for system metrics operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_snapshot(self, metrics_data: dict) -> SystemMetrics:
        """Create a new metrics snapshot.
        
        Args:
            metrics_data: Dictionary with metrics information
            
        Returns:
            Created SystemMetrics instance
        """
        metrics = SystemMetrics(**metrics_data)
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        return metrics
    
    def get_latest(self) -> Optional[SystemMetrics]:
        """Get the most recent metrics snapshot."""
        return (
            self.db.query(SystemMetrics)
            .order_by(desc(SystemMetrics.recorded_at))
            .first()
        )
    
    def get_time_series(self, hours: int = 24) -> List[SystemMetrics]:
        """Get metrics time series for the last N hours."""
        since = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.db.query(SystemMetrics)
            .filter(SystemMetrics.recorded_at >= since)
            .order_by(SystemMetrics.recorded_at)
            .all()
        )
