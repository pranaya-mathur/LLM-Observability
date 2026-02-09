"""Custom middleware for FastAPI."""

import time
import json
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge


# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)


# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
)

DETECTION_COUNT = Counter(
    'llm_detections_total',
    'Total LLM detections',
    ['tier', 'action'],
)

DETECTION_DURATION = Histogram(
    'llm_detection_duration_ms',
    'LLM detection duration in milliseconds',
    ['tier'],
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Number of active HTTP requests',
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for Prometheus metrics collection."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and collect metrics."""
        ACTIVE_REQUESTS.inc()
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Record metrics
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code,
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path,
            ).observe(duration)
            
            return response
        
        finally:
            ACTIVE_REQUESTS.dec()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request logging."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request details in structured format."""
        start_time = time.time()
        
        # Log request
        log_data = {
            "event": "request_started",
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
        }
        logger.info(json.dumps(log_data))
        
        try:
            response = await call_next(request)
            
            # Log response
            duration_ms = (time.time() - start_time) * 1000
            log_data = {
                "event": "request_completed",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
            logger.info(json.dumps(log_data))
            
            return response
        
        except Exception as e:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            log_data = {
                "event": "request_failed",
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
                "duration_ms": round(duration_ms, 2),
            }
            logger.error(json.dumps(log_data))
            raise
