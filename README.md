# LLM Observability

A work-in-progress observability system for monitoring LLM outputs and detecting potential issues.

## What it does

This project aims to detect problematic LLM outputs through multiple detection methods:
- Pattern matching for known issues
- Semantic similarity checks 
- LLM-based analysis for complex cases

Currently focused on detecting hallucinations, prompt injections, and unsupported claims.

## Status

Early development. Core detection works but needs refinement.

## Quick Start

```bash
pip install -r requirements.txt
python -m api.app
```

API will run on `http://localhost:8000`

Test endpoint:
```bash
curl -X POST http://localhost:8000/detect -H "Content-Type: application/json" -d '{"text": "test input"}'
```

## Configuration

Edit `config/policy.yaml` to change detection policies.

## Project Structure

```
LLM-Observability/
├── api/              # REST API endpoints
├── enforcement/      # Detection and policy logic  
├── signals/          # Individual detectors
├── agent/            # LLM agent for complex cases
├── config/           # Configuration files
└── tests/            # Tests (partial coverage)
```

## Known Issues

- Timeout issues with certain inputs on Windows
- Semantic detector initialization is slow on first run
- Test coverage incomplete
- No proper deployment setup yet
- Documentation needs work

## Todo

- [ ] Fix timeout handling
- [ ] Add proper logging
- [ ] Improve test coverage
- [ ] Add deployment docs
- [ ] Optimize performance
- [ ] Clean up code duplication

## Requirements

- Python 3.10+
- Optional: Ollama for LLM-based detection
- Optional: Groq API key

## Notes

This is a side project and not production-ready. Code quality varies. Some parts are experimental.

## License

MIT
