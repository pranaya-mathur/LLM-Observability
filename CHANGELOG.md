# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### In Progress
- FastAPI production wrapper
- Structured JSON logging
- Metrics dashboard
- Database persistence layer

## [0.3.0] - 2026-02-10

### Added
- Multi-tier detection system with cascading logic
- Semantic embedding detection (Tier 2)
- LLM agent for complex cases (Tier 3)
- Policy-driven enforcement via YAML configuration
- Decision caching for deterministic behavior
- Basic API endpoints for detection

### Fixed
- Timeout issues on pathological inputs
- Regex catastrophic backtracking problems
- Windows compatibility issues with timeouts
- False positives in acronym detection
- Database connection pooling delays

### Changed
- Simplified README and removed excessive formatting
- Improved error handling across all tiers
- Optimized semantic detector with input truncation
- Updated regex patterns for better security detection

## [0.2.0] - 2026-02-09

### Added
- LangGraph-based LLM agent
- Groq and Ollama provider support
- Decision caching system
- Prompt injection detection patterns
- Bias and toxicity detection

### Fixed
- Semantic detector initialization delays
- Memory leaks in embedding cache

## [0.1.0] - 2026-02-08

### Added
- Initial project structure
- Basic regex pattern detection
- Failure class taxonomy
- Policy configuration system
- Simple test suite

### Known Issues
- Performance degrades with very long inputs
- First request after startup is slow
- Limited test coverage
- No authentication on API endpoints

## Development Notes

### Architecture Evolution

The project started with simple regex patterns and evolved into a multi-tier system:

1. **Initial approach**: Pure regex matching
   - Fast but high false positive rate
   - Limited to known patterns

2. **Added semantic layer**: Embedding-based detection
   - Better handling of paraphrased content
   - Reduced false positives by ~30%
   - Added ~5-10ms latency

3. **Integrated LLM reasoning**: Agent for edge cases
   - Handles complex contextual cases
   - Fallback for ambiguous content
   - Expensive, used sparingly

### Performance Lessons

- Caching is critical for production use
- Regex patterns need careful testing for backtracking
- Embedding models are CPU-intensive on Windows
- Thread-based timeouts work better than signal-based
- Input preprocessing can prevent most timeout issues

### Design Decisions

- YAML for policies: Easy to modify without code changes
- Three tiers: Balance between speed and accuracy
- Fail-safe defaults: Allow on errors to avoid blocking valid content
- Stateless design: Easier to scale horizontally

## Future Direction

See TODO.md for detailed roadmap. Key focus areas:

- Improving test coverage
- Production hardening
- Performance optimization
- Better documentation
