# Test Suite for LLM Observability

## Overview

This directory contains comprehensive tests for Phase 1 and Phase 2 of the LLM Observability system.

## Test Files

### Unit Tests

- **test_langgraph_agent.py** - Tests for LangGraph agent functionality
  - Agent initialization
  - Normal prompt handling
  - Injection detection
  - Cache functionality
  - Cache statistics

- **test_llm_providers.py** - Tests for LLM provider integrations
  - Provider manager initialization
  - Groq provider availability
  - Ollama provider availability
  - LLM generation
  - Fallback mechanism

### Performance Tests

- **test_performance.py** - Performance and benchmark tests
  - Cache performance comparison
  - Batch processing
  - Concurrent request handling

### Integration Tests

- **test_integration.py** - End-to-end pipeline tests
  - SafeAgent integration
  - Control Tower pipeline
  - Signal detection

## Running Tests

### Run All Tests

```bash
# Using pytest (recommended)
pytest tests/ -v

# Or run individually
python tests/test_langgraph_agent.py
python tests/test_llm_providers.py
python tests/test_performance.py
python tests/test_integration.py
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/test_langgraph_agent.py tests/test_llm_providers.py -v

# Performance tests
python tests/test_performance.py

# Integration tests
python tests/test_integration.py
```

## Prerequisites

### Required Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest  # For running with pytest
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. **Setup LLM Provider (choose one):**

   **Option A: Groq (Cloud)**
   ```bash
   export GROQ_API_KEY="your_api_key"
   ```

   **Option B: Ollama (Local)**
   ```bash
   ollama serve
   ollama pull llama3.2
   ollama pull phi3
   ```

## Test Coverage

### Phase 1 (Embedding Detection)
- ✅ Embedding similarity computation
- ✅ Normal prompt handling
- ✅ Injection pattern detection

### Phase 2 (LLM Agent)
- ✅ LangGraph workflow execution
- ✅ Decision caching
- ✅ Multi-provider support
- ✅ Fallback mechanism
- ✅ Control Tower integration

## Expected Results

### All Tests Passing
```
✅ test_agent_initialization PASSED
✅ test_normal_prompt PASSED
✅ test_injection_detection PASSED
✅ test_cache_functionality PASSED
✅ test_provider_availability PASSED
✅ test_cache_performance PASSED
✅ test_control_tower_pipeline PASSED
```

### Common Warnings (Non-Critical)
```
⚠️  Groq provider not configured (set GROQ_API_KEY)
⚠️  Ollama not running (start with: ollama serve)
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run with output capture
pytest tests/ -v --tb=short
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r requirements.txt` |
| Groq tests fail | Set `GROQ_API_KEY` environment variable |
| Ollama tests fail | Start Ollama: `ollama serve` |
| Model not found | Pull models: `ollama pull phi3` |
| Slow tests | Groq is faster than Ollama for testing |

## Adding New Tests

1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use descriptive test function names: `test_feature_name()`
4. Add docstrings explaining what each test does
5. Include both positive and negative test cases
6. Update this README with new test descriptions

## Contact

For questions about tests, see the main README or create an issue.
