"""Failure classification taxonomy for LLM observability.

Defines standardized failure types that can be detected in LLM interactions.
Each failure class represents a specific pattern of problematic behavior.
"""

from enum import Enum


class FailureClass(str, Enum):
    """Enumeration of all detectable failure patterns in LLM responses."""
    
    # Critical failures - require immediate blocking
    FABRICATED_CONCEPT = "fabricated_concept"
    FABRICATED_FACT = "fabricated_fact"
    DANGEROUS_CONTENT = "dangerous_content"
    
    # High severity - strong warnings required
    MISSING_GROUNDING = "missing_grounding"
    DOMAIN_MISMATCH = "domain_mismatch"
    
    # Medium severity - user awareness needed
    OVERCONFIDENCE = "overconfidence"
    HEDGING_EXCESSIVE = "hedging_excessive"
    
    # Low severity - logging for analysis
    TONE_ISSUE = "tone_issue"
    FORMATTING_ISSUE = "formatting_issue"


class FailureMetadata:
    """Metadata describing characteristics of each failure class."""
    
    DESCRIPTIONS = {
        FailureClass.FABRICATED_CONCEPT: (
            "LLM invented a term, acronym, or concept that doesn't exist"
        ),
        FailureClass.FABRICATED_FACT: (
            "LLM stated a verifiably false fact with confidence"
        ),
        FailureClass.DANGEROUS_CONTENT: (
            "Response contains harmful, unsafe, or prohibited content"
        ),
        FailureClass.MISSING_GROUNDING: (
            "Response lacks citations, sources, or grounding in evidence"
        ),
        FailureClass.DOMAIN_MISMATCH: (
            "Response discusses wrong domain or misunderstands context"
        ),
        FailureClass.OVERCONFIDENCE: (
            "Response shows excessive certainty without justification"
        ),
        FailureClass.HEDGING_EXCESSIVE: (
            "Response is overly cautious with too many qualifiers"
        ),
        FailureClass.TONE_ISSUE: (
            "Response tone is inappropriate for context"
        ),
        FailureClass.FORMATTING_ISSUE: (
            "Response has structural or formatting problems"
        ),
    }
    
    @classmethod
    def get_description(cls, failure_class: FailureClass) -> str:
        """Get human-readable description of a failure class."""
        return cls.DESCRIPTIONS.get(failure_class, "Unknown failure class")
