# Phase 4: Production Deployment - Complete Guide

## Overview

Phase 4 brings production-ready features to the LLM Observability system:

- ✅ **FastAPI Application**: RESTful API with full CRUD operations
- ✅ **Database Persistence**: PostgreSQL/SQLite for logs and metrics
- ✅ **Prometheus Metrics**: Real-time monitoring and alerting
- ✅ **Docker Support**: Containerized deployment
- ✅ **Kubernetes Ready**: Scalable orchestration configs
- ✅ **Structured Logging**: JSON logs for production observability

## Quick Start

### Local Development (SQLite)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the API server (uses SQLite by default)
uvicorn api.main_v2:app --reload --port 8000

# 3. Access the API
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - Health: http://localhost:8000/health
```

### Production Setup (PostgreSQL)

```bash
# 1. Set up PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/llm_observability"

# 2. Initialize database
python -c "from persistence.database import init_db; init_db()"

# 3. Run with production settings
uvicorn api.main_v2:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Core Detection

#### POST /detect
Detect issues in a single LLM response.

**Request:**
```json
{
  "llm_response": "According to a study from Harvard, this approach is effective.",
  "context": {"query": "What's the best approach?"}
}
```

**Response:**
```json
{
  "action": "allow",
  "tier_used": 1,
  "method": "regex_strong",
  "confidence": 0.95,
  "processing_time_ms": 0.8,
  "failure_class": null,
  "severity": null,
  "explanation": "Strong citation pattern detected - legitimate source",
  "blocked": false
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "llm_response": "Test response",
    "context": {}
  }'
```

#### POST /detect/batch
Batch detection for up to 100 responses.

**Request:**
```json
[
  {"llm_response": "First response", "context": {}},
  {"llm_response": "Second response", "context": {}}
]
```

**Response:**
```json
{
  "total": 2,
  "results": [
    {"action": "allow", "tier_used": 1, "blocked": false, ...},
    {"action": "warn", "tier_used": 2, "blocked": false, ...}
  ]
}
```

### Monitoring & Health

#### GET /health
Health check with tier distribution.

**Response:**
```json
{
  "status": "healthy",
  "tier_distribution": {
    "tier1_pct": 95.2,
    "tier2_pct": 3.8,
    "tier3_pct": 1.0
  },
  "health_message": "✅ Healthy distribution"
}
```

#### GET /metrics/stats
Detailed detection statistics.

**Response:**
```json
{
  "total_detections": 1000,
  "tier1_count": 952,
  "tier2_count": 38,
  "tier3_count": 10,
  "distribution": {
    "tier1_pct": 95.2,
    "tier2_pct": 3.8,
    "tier3_pct": 1.0
  },
  "health": {
    "is_healthy": true,
    "message": "✅ Healthy distribution"
  }
}
```

#### GET /metrics
Prometheus metrics endpoint.

```bash
curl http://localhost:8000/metrics
```

#### GET /logs/recent?limit=50
Recent detection logs (max 500).

**Response:**
```json
{
  "total": 50,
  "logs": [
    {
      "id": 1,
      "tier_used": 1,
      "action": "allow",
      "blocked": false,
      "confidence": 0.95,
      "processing_time_ms": 0.8,
      "created_at": "2026-02-09T14:00:00"
    }
  ]
}
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t llm-observability:latest .

# Run with SQLite (development)
docker run -p 8000:8000 llm-observability:latest

# Run with PostgreSQL (production)
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@db:5432/llm_obs" \
  llm-observability:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://llm_user:llm_pass@db:5432/llm_observability
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=llm_user
      - POSTGRES_PASSWORD=llm_pass
      - POSTGRES_DB=llm_observability
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

## Kubernetes Deployment

### Prerequisites

```bash
# Ensure kubectl is configured
kubectl cluster-info
```

### Deploy to Kubernetes

```bash
# 1. Create namespace
kubectl create namespace llm-observability

# 2. Apply configurations
kubectl apply -f k8s/configmap.yaml -n llm-observability
kubectl apply -f k8s/postgres.yaml -n llm-observability
kubectl apply -f k8s/deployment.yaml -n llm-observability
kubectl apply -f k8s/service.yaml -n llm-observability

# 3. Check status
kubectl get pods -n llm-observability
kubectl get services -n llm-observability

# 4. Access the API
kubectl port-forward service/llm-observability-service 8000:80 -n llm-observability
```

### Scale Deployment

```bash
# Scale to 5 replicas
kubectl scale deployment llm-observability-api --replicas=5 -n llm-observability

# Auto-scale based on CPU
kubectl autoscale deployment llm-observability-api \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n llm-observability
```

## Database Schema

### DetectionLog Table

```sql
CREATE TABLE detection_logs (
    id SERIAL PRIMARY KEY,
    llm_response TEXT NOT NULL,
    context JSONB,
    action VARCHAR(20) NOT NULL,
    tier_used INTEGER NOT NULL,
    method VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    processing_time_ms FLOAT NOT NULL,
    failure_class VARCHAR(100),
    severity VARCHAR(20),
    explanation TEXT NOT NULL,
    blocked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    request_id VARCHAR(50)
);

CREATE INDEX idx_action ON detection_logs(action);
CREATE INDEX idx_tier_used ON detection_logs(tier_used);
CREATE INDEX idx_blocked ON detection_logs(blocked);
CREATE INDEX idx_created_at ON detection_logs(created_at);
```

### SystemMetrics Table

```sql
CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,
    total_detections INTEGER NOT NULL,
    tier1_count INTEGER NOT NULL,
    tier2_count INTEGER NOT NULL,
    tier3_count INTEGER NOT NULL,
    tier1_pct FLOAT NOT NULL,
    tier2_pct FLOAT NOT NULL,
    tier3_pct FLOAT NOT NULL,
    is_healthy BOOLEAN NOT NULL,
    health_message VARCHAR(200) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recorded_at ON system_metrics(recorded_at);
```

## Monitoring with Prometheus

### Prometheus Configuration

Add to `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'llm-observability'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Key Metrics

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `detection_tier_total{tier="1|2|3"}` - Detections per tier
- `detection_blocked_total` - Blocked responses
- `detection_processing_time_seconds` - Processing time distribution

### Grafana Dashboard

Import dashboard from `monitoring/grafana-dashboard.json` (to be created).

## Performance Tuning

### Workers Configuration

```bash
# Development (1 worker)
uvicorn api.main_v2:app --workers 1

# Production (CPU cores * 2 + 1)
uvicorn api.main_v2:app --workers 9  # For 4 CPU cores
```

### Database Connection Pool

In `persistence/database.py`:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,        # Adjust based on load
    max_overflow=10,     # Additional connections
    pool_pre_ping=True,  # Verify connections
)
```

### Caching Strategy

- Tier 1: LRU cache (99%+ hit rate)
- Tier 3: Decision cache (99%+ deterministic)
- Database: Connection pooling

## Testing the API

### Using HTTPie

```bash
# Install HTTPie
pip install httpie

# Test detection
http POST localhost:8000/detect \
  llm_response="Test response" \
  context:='{"query": "test"}'

# Check health
http GET localhost:8000/health

# Get stats
http GET localhost:8000/metrics/stats
```

### Using Python

```python
import requests

# Detection request
response = requests.post(
    "http://localhost:8000/detect",
    json={
        "llm_response": "According to Harvard research...",
        "context": {"query": "What works?"}
    }
)
print(response.json())

# Batch request
responses = [
    {"llm_response": "First", "context": {}},
    {"llm_response": "Second", "context": {}}
]
result = requests.post(
    "http://localhost:8000/detect/batch",
    json=responses
)
print(result.json())
```

## Environment Variables

```bash
# Database
DATABASE_URL="postgresql://user:pass@host:5432/db"  # or sqlite:///./db.db

# API Configuration
API_HOST="0.0.0.0"
API_PORT="8000"
API_WORKERS="4"

# Logging
LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT="json"  # json or text

# LLM Provider (for Tier 3)
GROQ_API_KEY="your-groq-api-key"  # Optional, falls back to Ollama
```

## Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql postgresql://user:pass@localhost:5432/llm_observability

# Check SQLite file
ls -lh llm_observability.db
sqlite3 llm_observability.db "SELECT COUNT(*) FROM detection_logs;"
```

### API Not Starting

```bash
# Check logs
docker logs <container-id>

# Verify dependencies
pip list | grep -E "fastapi|uvicorn|sqlalchemy"

# Test import
python -c "from api.main_v2 import app; print('OK')"
```

### High Memory Usage

- Reduce worker count
- Lower database connection pool size
- Enable response streaming for large batches
- Monitor with `/metrics` endpoint

## Production Checklist

- [ ] Database: PostgreSQL configured with proper credentials
- [ ] CORS: Update `allow_origins` in middleware
- [ ] Environment: Set `DATABASE_URL` and `GROQ_API_KEY`
- [ ] Monitoring: Prometheus scraping `/metrics`
- [ ] Logging: Structured JSON logs enabled
- [ ] Security: API behind reverse proxy (nginx/traefik)
- [ ] SSL/TLS: HTTPS certificates configured
- [ ] Rate Limiting: Implement request throttling
- [ ] Backup: Database backup strategy in place
- [ ] Health Checks: Load balancer monitoring `/health`

## Next Steps

- [ ] Add authentication (JWT/OAuth2)
- [ ] Implement rate limiting per client
- [ ] Add API versioning (/v1, /v2)
- [ ] Create Grafana dashboards
- [ ] Set up CI/CD pipeline
- [ ] Add integration tests
- [ ] Document API with OpenAPI 3.0 spec
- [ ] Implement request caching
- [ ] Add async batch processing queue
- [ ] Create admin dashboard

## Support

For issues or questions:
- GitHub Issues: [pranaya-mathur/LLM-Observability](https://github.com/pranaya-mathur/LLM-Observability/issues)
- Email: pranaya.mathur@yahoo.com

## License

MIT License - See LICENSE file for details.
