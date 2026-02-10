# TODO

Tracking work items and future improvements.

## High Priority

- [ ] Add comprehensive integration tests for API endpoints
- [ ] Implement rate limiting per user/API key
- [ ] Add Prometheus metrics exporter
- [ ] Write performance benchmarking suite
- [ ] Document deployment architecture

## API Improvements

- [ ] Add batch detection endpoint
- [ ] Implement streaming responses for long texts
- [ ] Add webhook support for async notifications
- [ ] Create OpenAPI/Swagger documentation
- [ ] Add API versioning (v1, v2)

## Detection Enhancements

- [ ] Fine-tune semantic similarity thresholds
- [ ] Add support for custom regex patterns via API
- [ ] Implement confidence score calibration
- [ ] Add multilingual support
- [ ] Create detection pattern marketplace/registry

## Performance

- [ ] Profile and optimize hot paths
- [ ] Implement connection pooling for external services
- [ ] Add Redis caching layer
- [ ] Optimize embedding model loading
- [ ] Reduce cold start time

## Monitoring & Observability

- [ ] Add structured JSON logging
- [ ] Implement distributed tracing with OpenTelemetry
- [ ] Create Grafana dashboards
- [ ] Add alerting for anomalies
- [ ] Track detection accuracy over time

## Infrastructure

- [ ] Create Kubernetes deployment manifests
- [ ] Add Helm charts
- [ ] Set up CI/CD pipeline
- [ ] Add database migrations with Alembic
- [ ] Create Docker Compose for local development

## Security

- [ ] Add OAuth2/JWT authentication
- [ ] Implement API key rotation
- [ ] Add audit logging
- [ ] Security audit of all dependencies
- [ ] Add HTTPS enforcement in production

## Documentation

- [ ] Add architecture decision records (ADRs)
- [ ] Create video tutorials
- [ ] Write deployment guide
- [ ] Document common use cases
- [ ] Add troubleshooting guide

## Testing

- [ ] Increase test coverage to 80%+
- [ ] Add property-based tests with Hypothesis
- [ ] Create load testing suite
- [ ] Add security testing (OWASP)
- [ ] Implement mutation testing

## Nice to Have

- [ ] Web UI for configuration management
- [ ] A/B testing framework
- [ ] Auto-tuning of detection thresholds
- [ ] Plugin system for custom detectors
- [ ] Export detection reports as PDF

## Research & Exploration

- [ ] Evaluate newer embedding models
- [ ] Research federated learning for privacy
- [ ] Explore quantized models for faster inference
- [ ] Investigate active learning for pattern updates
- [ ] Study adversarial robustness

## Bug Fixes Needed

- [ ] Fix occasional timeout on Windows with large inputs
- [ ] Handle edge case with empty responses
- [ ] Improve error messages for configuration issues
- [ ] Fix memory leak in long-running processes

---

Last updated: 2026-02-11
