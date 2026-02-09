"""Tier-based routing for 3-tier detection architecture.

Routes requests to appropriate tier based on confidence levels:
- Tier 1 (95%): Deterministic regex (fast)
- Tier 2 (4%): Semantic embeddings (medium)
- Tier 3 (1%): LLM agents (slow but accurate)
"""

from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class TierDecision:
    """Decision about which tier to use."""
    tier: int
    method: str
    reason: str
    confidence: float


class TierRouter:
    """Routes detection requests to appropriate tier."""
    
    def __init__(
        self,
        tier1_strong_threshold: float = 0.8,
        tier1_weak_threshold: float = 0.3,
        tier2_threshold: float = 0.75
    ):
        """
        Initialize tier router with confidence thresholds.
        
        Args:
            tier1_strong_threshold: Strong pattern confidence (>=0.8)
            tier1_weak_threshold: Anti-pattern confidence (<=0.3)
            tier2_threshold: Semantic detection confidence (0.75)
        """
        self.tier1_strong = tier1_strong_threshold
        self.tier1_weak = tier1_weak_threshold
        self.tier2_threshold = tier2_threshold
        
        # Tracking for 95/4/1 distribution
        self.tier_stats = {
            "tier1": 0,
            "tier2": 0,
            "tier3": 0,
            "total": 0
        }
    
    def route(self, initial_result: Dict[str, Any]) -> TierDecision:
        """
        Determine which tier should handle this request.
        
        Args:
            initial_result: Result from initial detection attempt
            
        Returns:
            TierDecision with tier number and reasoning
        """
        confidence = initial_result.get("confidence", 0.0)
        method = initial_result.get("method", "unknown")
        
        # Tier 1: Strong confidence from regex
        if method == "regex_strong" and confidence >= self.tier1_strong:
            self._record_tier(1)
            return TierDecision(
                tier=1,
                method="regex_strong",
                reason="High confidence regex pattern match",
                confidence=confidence
            )
        
        # Tier 1: Clear anti-pattern
        if method == "regex_anti" and confidence >= self.tier1_strong:
            self._record_tier(1)
            return TierDecision(
                tier=1,
                method="regex_anti",
                reason="Clear anti-pattern detected",
                confidence=confidence
            )
        
        # Tier 2: Gray zone - use semantic detection
        if self.tier1_weak < confidence < self.tier1_strong:
            self._record_tier(2)
            return TierDecision(
                tier=2,
                method="semantic",
                reason="Gray zone - requires semantic analysis",
                confidence=confidence
            )
        
        # Tier 3: Edge case - use LLM agent
        self._record_tier(3)
        return TierDecision(
            tier=3,
            method="llm_agent",
            reason="Edge case requiring multi-step reasoning",
            confidence=confidence
        )
    
    def _record_tier(self, tier: int):
        """Record tier usage for statistics."""
        self.tier_stats[f"tier{tier}"] += 1
        self.tier_stats["total"] += 1
    
    def get_distribution(self) -> Dict[str, float]:
        """
        Get current tier distribution percentages.
        
        Returns:
            Dict with tier1_pct, tier2_pct, tier3_pct
        """
        total = self.tier_stats["total"]
        if total == 0:
            return {"tier1_pct": 0.0, "tier2_pct": 0.0, "tier3_pct": 0.0, "total_requests": 0}
        
        return {
            "tier1_pct": (self.tier_stats["tier1"] / total) * 100,
            "tier2_pct": (self.tier_stats["tier2"] / total) * 100,
            "tier3_pct": (self.tier_stats["tier3"] / total) * 100,
            "total_requests": total
        }
    
    def check_distribution_health(self) -> Tuple[bool, str]:
        """
        Check if tier distribution is healthy (target: 95/4/1).
        
        Returns:
            Tuple of (is_healthy, status_message)
        """
        dist = self.get_distribution()
        
        if dist["total_requests"] < 100:
            return True, "Not enough data for health check (need 100+ requests)"
        
        tier1 = dist["tier1_pct"]
        tier2 = dist["tier2_pct"]
        tier3 = dist["tier3_pct"]
        
        # Healthy ranges (with tolerance)
        tier1_healthy = 92 <= tier1 <= 98  # Target: 95%
        tier2_healthy = 2 <= tier2 <= 7    # Target: 4%
        tier3_healthy = 0 <= tier3 <= 3    # Target: 1%
        
        if tier1_healthy and tier2_healthy and tier3_healthy:
            return True, f"✅ Healthy distribution - Tier1: {tier1:.1f}%, Tier2: {tier2:.1f}%, Tier3: {tier3:.1f}%"
        
        warnings = []
        if not tier1_healthy:
            warnings.append(f"⚠️ Tier1 at {tier1:.1f}% (target: 95%)")
        if not tier2_healthy:
            warnings.append(f"⚠️ Tier2 at {tier2:.1f}% (target: 4%)")
        if not tier3_healthy:
            warnings.append(f"⚠️ Tier3 at {tier3:.1f}% (target: 1%)")
        
        return False, " | ".join(warnings)
    
    def reset_stats(self):
        """Reset tier statistics."""
        self.tier_stats = {"tier1": 0, "tier2": 0, "tier3": 0, "total": 0}
