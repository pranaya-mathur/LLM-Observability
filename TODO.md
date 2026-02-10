# Development Roadmap

## High Priority

- [ ] Improve regex pattern efficiency for large inputs
- [ ] Add more comprehensive test coverage (currently ~60%)
- [ ] Optimize semantic embedding caching strategy
- [ ] Fix timeout issues on Windows for pathological inputs
- [ ] Document API endpoints properly with OpenAPI spec

## API Improvements

- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add request validation middleware
- [ ] Better error messages and status codes
- [ ] Add health check endpoint
- [ ] Metrics endpoint for monitoring

## Detection Enhancements

- [ ] Add more sophisticated prompt injection patterns
- [ ] Improve false positive rate on citations
- [ ] Add support for multi-language content
- [ ] Better handling of code snippets in responses
- [ ] Add confidence scores to all detections

## Performance

- [ ] Profile Tier 2 embedding performance
- [ ] Investigate async processing for Tier 3
- [ ] Add connection pooling for LLM providers
- [ ] Benchmark against different input sizes
- [ ] Memory profiling and optimization

## Infrastructure

- [ ] Add Docker Compose for local development
- [ ] Create Kubernetes deployment manifests
- [ ] Set up CI/CD pipeline
- [ ] Add production-ready logging (structured JSON)
- [ ] Implement distributed tracing

## Documentation

- [ ] Add architecture decision records (ADRs)
- [ ] Create usage examples for common scenarios
- [ ] Document configuration options
- [ ] Add troubleshooting guide
- [ ] Write deployment guide

## Testing

- [ ] Add integration tests
- [ ] Add load testing scenarios
- [ ] Test edge cases more thoroughly
- [ ] Add mutation testing
- [ ] Create regression test suite

## Nice to Have

- [ ] Web UI for policy management
- [ ] Real-time dashboard for detection statistics
- [ ] A/B testing framework for detection strategies
- [ ] Plugin system for custom detectors
- [ ] Export metrics to Prometheus
- [ ] Support for custom LLM providers

## Known Issues

- Semantic detector can timeout on very long repetitive text
- First request after startup is slow due to model loading
- SQLite performance issues with high concurrency
- Some regex patterns can cause catastrophic backtracking
- Cache doesn't persist across restarts

## Research Ideas

- Investigate active learning for improving detection
- Explore lightweight models for Tier 2
- Research optimal threshold tuning strategies
- Study false positive patterns in production
- Evaluate alternative embedding models
