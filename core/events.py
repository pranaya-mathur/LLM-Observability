from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class LLMRequestEvent(BaseModel):
    schema_version: str = "v1"
    request_id: UUID
    trace_id: UUID
    timestamp: datetime
    provider: str
    model: str
    prompt: Dict[str, Any]
    params: Dict[str, Any]

class LLMResponseEvent(BaseModel):
    schema_version: str = "v1"
    request_id: UUID
    timestamp: datetime
    latency_ms: int
    response_text: Optional[str]
    error: Optional[str]
