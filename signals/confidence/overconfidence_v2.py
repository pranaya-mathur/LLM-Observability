"""Hybrid overconfidence detector using regex + embeddings.

Detects when LLM is excessively confident without proper justification.
"""

from signals.embeddings.semantic_detector import SemanticDetector
from typing import Dict, Any
import re
import logging

logger = logging.getLogger(__name__)


class OverconfidenceV2Signal:
    """Hybrid overconfidence detection."""
    
    name = "overconfidence"
    
    def __init__(self):
        """Initialize with semantic detector."""
        self.semantic_detector = SemanticDetector()
        
        # Strong overconfidence markers
        self.strong_markers = [
            r'\b(absolutely|definitely|certainly|undoubtedly)\s+(true|correct|will|is)\b',
            r'\b100%\s+(sure|certain|guaranteed)\b',
            r'\bthere is no (doubt|question|possibility)\b',
            r'\balways\s+(true|correct|happens)\b',
            r'\bnever\s+(wrong|fails|incorrect)\b',
            r'\bimpossible\s+to\s+be\s+wrong\b',
        ]
        
        # Weak hedging (indicates proper uncertainty)
        self.hedging_markers = [
            'may', 'might', 'could', 'possibly', 'perhaps',
            'likely', 'probably', 'seems', 'appears',
            'suggests', 'indicates', 'some evidence'
        ]
    
    def extract(self, prompt: str, response: str, metadata: dict) -> Dict[str, Any]:
        """Detect overconfidence patterns.
        
        Args:
            prompt: User prompt
            response: LLM response
            metadata: Additional context
            
        Returns:
            Signal dictionary
        """
        if not response or len(response.strip()) < 20:
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.0,
                "explanation": "Response too short",
                "method": "length_check"
            }
        
        response_lower = response.lower()
        
        # Check for strong overconfidence markers
        strong_marker_count = sum(
            1 for pattern in self.strong_markers
            if re.search(pattern, response_lower)
        )
        
        if strong_marker_count >= 2:
            return {
                "signal": self.name,
                "value": True,
                "confidence": 0.85,
                "explanation": f"Multiple strong overconfidence markers ({strong_marker_count})",
                "method": "regex_strong"
            }
        
        # Check for hedging (indicates appropriate uncertainty)
        hedging_count = sum(
            1 for marker in self.hedging_markers
            if marker in response_lower
        )
        
        if hedging_count >= 3:
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.8,
                "explanation": f"Appropriate hedging found ({hedging_count} markers)",
                "method": "regex_hedged"
            }
        
        # Gray zone: Use semantic detection
        if strong_marker_count == 1 or hedging_count in [1, 2]:
            semantic_result = self.semantic_detector.detect(
                response,
                "overconfidence",
                threshold=0.72
            )
            
            return {
                "signal": self.name,
                "value": semantic_result["detected"],
                "confidence": semantic_result["confidence"],
                "explanation": f"Mixed signals, semantic analysis: {semantic_result['explanation']}",
                "method": "hybrid_semantic"
            }
        
        # No clear signals
        return {
            "signal": self.name,
            "value": False,
            "confidence": 0.4,
            "explanation": "No clear overconfidence patterns",
            "method": "default"
        }
