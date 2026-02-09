"""Pydantic models for API request/response."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class DetectionRequest(BaseModel):
    """Request model for LLM response detection."""
    
    llm_response: str = Field(
        ...,
        description="The LLM response text to analyze",
        min_length=1,
        max_length=50000,
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional context information (e.g., query, metadata)",
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "llm_response": "According to a study from Harvard, this approach is effective.",
                "context": {"query": "What's the best approach?"},
            }
        }


class DetectionResponse(BaseModel):
    """Response model for detection results."""
    
    action: str = Field(..., description="Action to take: allow, warn, block, log")
    tier_used: int = Field(..., description="Which tier was used (1, 2, or 3)")
    method: str = Field(..., description="Detection method used")
    confidence: float = Field(..., description="Confidence score (0.0 - 1.0)")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    failure_class: Optional[str] = Field(None, description="Type of failure detected")
    severity: Optional[str] = Field(None, description="Severity level")
    explanation: str = Field(..., description="Human-readable explanation")
    blocked: bool = Field(..., description="Whether response was blocked")
    
    class Config:
        json_schema_extra = {
            "example": {
                "action": "allow",
                "tier_used": 1,
                "method": "regex_strong",
                "confidence": 0.95,
                "processing_time_ms": 0.8,
                "failure_class": None,
                "severity": None,
                "explanation": "Strong citation pattern detected - legitimate source",
                "blocked": False,
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Health status: healthy, degraded, unhealthy")
    tier_distribution: Dict[str, float] = Field(..., description="Current tier distribution percentages")
    health_message: str = Field(..., description="Health status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "tier_distribution": {
                    "tier1_pct": 95.2,
                    "tier2_pct": 3.8,
                    "tier3_pct": 1.0,
                },
                "health_message": "✅ Healthy distribution",
            }
        }


class StatsResponse(BaseModel):
    """Response model for detection statistics."""
    
    total_detections: int = Field(..., description="Total number of detections")
    tier1_count: int = Field(..., description="Tier 1 detection count")
    tier2_count: int = Field(..., description="Tier 2 detection count")
    tier3_count: int = Field(..., description="Tier 3 detection count")
    distribution: Dict[str, float] = Field(..., description="Tier distribution percentages")
    health: Dict[str, Any] = Field(..., description="Health status information")
