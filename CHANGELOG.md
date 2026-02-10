# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Multi-tier detection architecture with cascading fallback
- Semantic embedding-based detection for ambiguous cases
- LLM agent integration for complex reasoning
- Policy-driven enforcement via YAML configuration
- FastAPI endpoints for detection
- Caching system for deterministic responses
- Health monitoring and statistics tracking

### Changed
- Improved regex patterns to handle edge cases
- Optimized embedding initialization to reduce latency
- Enhanced timeout handling for long-running detections
- Refactored API structure for better maintainability

### Fixed
- Regex catastrophic backtracking on pathological inputs
- Windows compatibility issues with signal handling
- Database connection pooling delays
- HuggingFace model loading network calls
- False positives in acronym detection patterns
- Thread cleanup in timeout handlers

## [0.2.0] - 2026-02-10

### Added
- Tier 2 semantic detection with sentence transformers
- Tier 3 LLM agent with decision caching
- Prompt injection detection
- Bias and toxicity detection modules
- Comprehensive test suite
- API authentication and authorization

### Fixed
- Input validation and sanitization
- SQL injection and XSS pattern detection
- Path traversal detection
- Email validation for development domains

## [0.1.0] - 2026-02-08

### Added
- Initial project structure
- Basic regex-based detection (Tier 1)
- Policy configuration system
- Core failure class definitions
- Basic API server with FastAPI
- Docker support
- Initial documentation

### Security
- Added input length limits
- Implemented timeout protection
- Added rate limiting middleware
