"""Embedding-based semantic detection module.

Provides deterministic semantic similarity detection using sentence transformers.
This is Tier 1 of the hybrid architecture - fast and deterministic.
"""

from .semantic_detector import SemanticDetector

__all__ = ['SemanticDetector']
