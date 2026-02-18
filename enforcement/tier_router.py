"""Tier routing logic for 3-tier detection system.

Routes requests to appropriate detection tier based on confidence:
- Tier 1: High confidence regex matches (>80%)
- Tier 2: Medium confidence semantic analysis (15-80%)
- Tier 3: Low/uncertain confidence LLM reasoning (<15% or gray zone)
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple


@dataclass
class TierDecision:
    """Decision about which tier to use."""
    tier: int  # 1, 2, or 3
    reason: str  # Why this tier was chosen


class TierRouter:
    """Routes detection requests to appropriate tier based on confidence."""
    
    def __init__(self):
        """Initialize tier router with statistics tracking."""
        self.tier_stats = {
            "total": 0,
            "tier1": 0,
            "tier2": 0,
            "tier3": 0
        }
    
    def route(self, tier1_result: Dict[str, Any]) -> TierDecision:
        """Route to appropriate tier based on Tier 1 confidence.
        
        Routing Logic:
        - Tier 1 (>80%): Strong regex match, decision final
        - Tier 3 (5-15%): Gray zone, needs LLM deep reasoning
        - Tier 2 (15-80%): Medium confidence, semantic analysis sufficient
        - Tier 3 (<5%): Very uncertain, needs LLM analysis
        
        Args:
            tier1_result: Result dictionary from Tier 1 detection
            
        Returns:
            TierDecision indicating which tier to use
        """
        self.tier_stats["total"] += 1
        
        confidence = tier1_result.get("confidence", 0.5)
        should_allow = tier1_result.get("should_allow")
        failure_class = tier1_result.get("failure_class")
        
        # Tier 1: High confidence match (>80%)
        # Strong regex detection - decision is final
        if confidence >= 0.80:
            self.tier_stats["tier1"] += 1
            return TierDecision(
                tier=1, 
                reason=f"High confidence regex match ({confidence:.0%})"
            )
        
        # Tier 3: Gray zone (5-15% confidence)
        # This is where dangerous content often falls - needs LLM analysis
        # Examples: "stop taking insulin" (9.8%), subtle medical misinformation
        elif 0.05 <= confidence < 0.15:
            self.tier_stats["tier3"] += 1
            return TierDecision(
                tier=3,
                reason=f"Gray zone confidence ({confidence:.0%}) - needs LLM reasoning"
            )
        
        # Tier 2: Medium confidence (15-80%)
        # Semantic analysis should be sufficient
        elif 0.15 <= confidence < 0.80:
            self.tier_stats["tier2"] += 1
            return TierDecision(
                tier=2,
                reason=f"Medium confidence ({confidence:.0%}) - semantic analysis"
            )
        
        # Tier 3: Very low confidence (<5%)
        # Too uncertain - needs deep LLM reasoning
        else:
            self.tier_stats["tier3"] += 1
            return TierDecision(
                tier=3,
                reason=f"Very low confidence ({confidence:.0%}) - needs deep analysis"
            )
    
    def get_distribution(self) -> Dict[str, float]:
        """Get percentage distribution across tiers.
        
        Returns:
            Dictionary with tier percentages
        """
        total = self.tier_stats["total"]
        if total == 0:
            return {
                "tier1_pct": 0.0,
                "tier2_pct": 0.0,
                "tier3_pct": 0.0
            }
        
        return {
            "tier1_pct": (self.tier_stats["tier1"] / total) * 100,
            "tier2_pct": (self.tier_stats["tier2"] / total) * 100,
            "tier3_pct": (self.tier_stats["tier3"] / total) * 100
        }
    
    def check_distribution_health(self) -> Tuple[bool, str]:
        """Check if tier distribution is healthy (close to 95/4/1 target).
        
        Returns:
            Tuple of (is_healthy, message)
        """
        dist = self.get_distribution()
        
        # Target: 95% Tier 1, 4% Tier 2, 1% Tier 3
        # Allow some variance: Tier 1 (90-98%), Tier 2 (2-8%), Tier 3 (0-5%)
        tier1_ok = 90 <= dist["tier1_pct"] <= 98
        tier2_ok = 2 <= dist["tier2_pct"] <= 8
        tier3_ok = 0 <= dist["tier3_pct"] <= 5
        
        if tier1_ok and tier2_ok and tier3_ok:
            return True, "Distribution healthy (close to 95/4/1 target)"
        
        # Generate helpful message
        issues = []
        if not tier1_ok:
            issues.append(f"Tier 1: {dist['tier1_pct']:.1f}% (target: 90-98%)")
        if not tier2_ok:
            issues.append(f"Tier 2: {dist['tier2_pct']:.1f}% (target: 2-8%)")
        if not tier3_ok:
            issues.append(f"Tier 3: {dist['tier3_pct']:.1f}% (target: 0-5%)")
        
        return False, f"Distribution issues: {', '.join(issues)}"
    
    def reset_stats(self):
        """Reset tier statistics."""
        self.tier_stats = {
            "total": 0,
            "tier1": 0,
            "tier2": 0,
            "tier3": 0
        }
