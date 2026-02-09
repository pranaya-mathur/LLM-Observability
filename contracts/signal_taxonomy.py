"""Signal taxonomy - Static analysis definitions for LLM outputs.

Signals are deterministic detectors that analyze LLM responses.
They don't make decisions - they provide evidence.

Signals = Static Analysis for LLMs
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contracts.failure_classes import FailureClass
from contracts.severity_levels import SeverityLevel


class SignalCategory(str, Enum):
    """High-level categories for signal types."""
    
    SEMANTIC = "semantic"          # Meaning and accuracy
    GROUNDING = "grounding"        # Citations and evidence
    DOMAIN = "domain"              # Topic and context
    CONFIDENCE = "confidence"      # Certainty and hedging
    SAFETY = "safety"              # Harmful content
    QUALITY = "quality"            # Formatting and tone


@dataclass
class SignalDefinition:
    """Formal definition of a signal detector.
    
    Signals are deterministic analyzers that:
    1. Take prompt + response as input
    2. Return structured detection result
    3. Don't make enforcement decisions
    4. Provide evidence for policy engine
    """
    
    name: str
    category: SignalCategory
    failure_class: FailureClass
    severity_hint: SeverityLevel
    description: str
    trigger_conditions: str
    
    # Confidence thresholds
    high_confidence_threshold: float = 0.8
    medium_confidence_threshold: float = 0.6
    low_confidence_threshold: float = 0.4
    
    def __post_init__(self):
        """Validate signal definition."""
        assert 0.0 <= self.high_confidence_threshold <= 1.0
        assert 0.0 <= self.medium_confidence_threshold <= 1.0
        assert 0.0 <= self.low_confidence_threshold <= 1.0


class SignalTaxonomy:
    """Registry of all signal definitions.
    
    Provides single source of truth for what signals exist
    and what they detect.
    """
    
    SIGNALS: Dict[str, SignalDefinition] = {
        
        # ============================================
        # SEMANTIC SIGNALS
        # ============================================
        
        "fabricated_concept": SignalDefinition(
            name="fabricated_concept",
            category=SignalCategory.SEMANTIC,
            failure_class=FailureClass.FABRICATED_CONCEPT,
            severity_hint=SeverityLevel.CRITICAL,
            description="Detects invented terms, acronyms, or concepts",
            trigger_conditions="""
            - Suspicious acronym expansions
            - Non-existent technical terms
            - Fake company/product names
            - Made-up scientific concepts
            """,
            high_confidence_threshold=0.75,
            medium_confidence_threshold=0.60,
            low_confidence_threshold=0.45,
        ),
        
        "fabricated_fact": SignalDefinition(
            name="fabricated_fact",
            category=SignalCategory.SEMANTIC,
            failure_class=FailureClass.FABRICATED_FACT,
            severity_hint=SeverityLevel.CRITICAL,
            description="Detects false statements presented as facts",
            trigger_conditions="""
            - Incorrect dates or statistics
            - Misattributed quotes
            - Fake historical events
            - Verifiably false claims
            """,
            high_confidence_threshold=0.80,
            medium_confidence_threshold=0.65,
            low_confidence_threshold=0.50,
        ),
        
        # ============================================
        # GROUNDING SIGNALS
        # ============================================
        
        "missing_grounding": SignalDefinition(
            name="missing_grounding",
            category=SignalCategory.GROUNDING,
            failure_class=FailureClass.MISSING_GROUNDING,
            severity_hint=SeverityLevel.HIGH,
            description="Detects lack of citations or evidence",
            trigger_conditions="""
            - No source attribution
            - Factual claims without references
            - Missing citations for statistics
            - Unverified assertions
            """,
            high_confidence_threshold=0.70,
            medium_confidence_threshold=0.55,
            low_confidence_threshold=0.40,
        ),
        
        # ============================================
        # DOMAIN SIGNALS
        # ============================================
        
        "domain_mismatch": SignalDefinition(
            name="domain_mismatch",
            category=SignalCategory.DOMAIN,
            failure_class=FailureClass.DOMAIN_MISMATCH,
            severity_hint=SeverityLevel.HIGH,
            description="Detects wrong topic or context misunderstanding",
            trigger_conditions="""
            - Response in completely different domain
            - Context misinterpretation
            - Wrong field of expertise applied
            - Unrelated topic discussed
            """,
            high_confidence_threshold=0.75,
            medium_confidence_threshold=0.60,
            low_confidence_threshold=0.45,
        ),
        
        # ============================================
        # CONFIDENCE SIGNALS
        # ============================================
        
        "overconfidence": SignalDefinition(
            name="overconfidence",
            category=SignalCategory.CONFIDENCE,
            failure_class=FailureClass.OVERCONFIDENCE,
            severity_hint=SeverityLevel.MEDIUM,
            description="Detects excessive certainty without justification",
            trigger_conditions="""
            - Absolute statements without qualification
            - No acknowledgment of uncertainty
            - Overly definitive predictions
            - Missing epistemic humility
            """,
            high_confidence_threshold=0.70,
            medium_confidence_threshold=0.55,
            low_confidence_threshold=0.40,
        ),
        
        "hedging_excessive": SignalDefinition(
            name="hedging_excessive",
            category=SignalCategory.CONFIDENCE,
            failure_class=FailureClass.HEDGING_EXCESSIVE,
            severity_hint=SeverityLevel.MEDIUM,
            description="Detects too much hedging reducing utility",
            trigger_conditions="""
            - Every sentence has qualifiers
            - Overly cautious language
            - Too many 'maybe', 'possibly', 'might'
            - Unhelpful due to excessive caution
            """,
            high_confidence_threshold=0.65,
            medium_confidence_threshold=0.50,
            low_confidence_threshold=0.35,
        ),
        
        # ============================================
        # SAFETY SIGNALS
        # ============================================
        
        "dangerous_content": SignalDefinition(
            name="dangerous_content",
            category=SignalCategory.SAFETY,
            failure_class=FailureClass.DANGEROUS_CONTENT,
            severity_hint=SeverityLevel.CRITICAL,
            description="Detects harmful or prohibited content",
            trigger_conditions="""
            - Harmful instructions
            - Dangerous advice
            - Discriminatory language
            - Violence or illegal content
            """,
            high_confidence_threshold=0.85,
            medium_confidence_threshold=0.70,
            low_confidence_threshold=0.55,
        ),
        
        # ============================================
        # QUALITY SIGNALS
        # ============================================
        
        "tone_issue": SignalDefinition(
            name="tone_issue",
            category=SignalCategory.QUALITY,
            failure_class=FailureClass.TONE_ISSUE,
            severity_hint=SeverityLevel.LOW,
            description="Detects inappropriate tone for context",
            trigger_conditions="""
            - Too formal or too casual
            - Inappropriate humor
            - Inconsistent personality
            - Context-inappropriate style
            """,
            high_confidence_threshold=0.60,
            medium_confidence_threshold=0.45,
            low_confidence_threshold=0.30,
        ),
        
        "formatting_issue": SignalDefinition(
            name="formatting_issue",
            category=SignalCategory.QUALITY,
            failure_class=FailureClass.FORMATTING_ISSUE,
            severity_hint=SeverityLevel.LOW,
            description="Detects structural or formatting problems",
            trigger_conditions="""
            - Broken markdown
            - Inconsistent list formatting
            - Poor structure
            - Readability issues
            """,
            high_confidence_threshold=0.65,
            medium_confidence_threshold=0.50,
            low_confidence_threshold=0.35,
        ),
    }
    
    @classmethod
    def get_signal(cls, signal_name: str) -> Optional[SignalDefinition]:
        """Get signal definition by name."""
        return cls.SIGNALS.get(signal_name)
    
    @classmethod
    def get_by_category(cls, category: SignalCategory) -> Dict[str, SignalDefinition]:
        """Get all signals in a category."""
        return {
            name: sig for name, sig in cls.SIGNALS.items()
            if sig.category == category
        }
    
    @classmethod
    def get_by_severity(cls, severity: SeverityLevel) -> Dict[str, SignalDefinition]:
        """Get all signals with given severity hint."""
        return {
            name: sig for name, sig in cls.SIGNALS.items()
            if sig.severity_hint == severity
        }
    
    @classmethod
    def list_all(cls) -> Dict[str, SignalDefinition]:
        """Get all signal definitions."""
        return cls.SIGNALS.copy()
