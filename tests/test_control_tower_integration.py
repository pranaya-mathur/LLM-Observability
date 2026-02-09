"""Unit tests for ControlTowerV3 to ensure API compatibility."""

import pytest
from enforcement.control_tower_v3 import ControlTowerV3


class TestControlTowerV3Stats:
    """Test ControlTowerV3 statistics methods."""
    
    def test_get_tier_stats_structure(self):
        """Test that get_tier_stats() returns all required keys."""
        ct = ControlTowerV3()
        stats = ct.get_tier_stats()
        
        # Check top-level keys
        assert "total" in stats, "Missing 'total' key"
        assert "tier1_count" in stats, "Missing 'tier1_count' key"
        assert "tier2_count" in stats, "Missing 'tier2_count' key"
        assert "tier3_count" in stats, "Missing 'tier3_count' key"
        assert "distribution" in stats, "Missing 'distribution' key"
        assert "health" in stats, "Missing 'health' key"
        assert "tier_availability" in stats, "Missing 'tier_availability' key"
    
    def test_get_tier_stats_distribution_structure(self):
        """Test that distribution dict has required keys."""
        ct = ControlTowerV3()
        stats = ct.get_tier_stats()
        distribution = stats["distribution"]
        
        assert "tier1_pct" in distribution
        assert "tier2_pct" in distribution
        assert "tier3_pct" in distribution
    
    def test_get_tier_stats_health_structure(self):
        """Test that health dict has required keys."""
        ct = ControlTowerV3()
        stats = ct.get_tier_stats()
        health = stats["health"]
        
        assert "is_healthy" in health
        assert "message" in health
        assert isinstance(health["is_healthy"], bool)
        assert isinstance(health["message"], str)
    
    def test_get_tier_stats_initial_values(self):
        """Test initial values when no detections have been made."""
        ct = ControlTowerV3()
        stats = ct.get_tier_stats()
        
        # Initially, all counts should be 0
        assert stats["total"] == 0
        assert stats["tier1_count"] == 0
        assert stats["tier2_count"] == 0
        assert stats["tier3_count"] == 0
        
        # Percentages should be 0
        assert stats["distribution"]["tier1_pct"] == 0.0
        assert stats["distribution"]["tier2_pct"] == 0.0
        assert stats["distribution"]["tier3_pct"] == 0.0
    
    def test_get_tier_stats_data_types(self):
        """Test that all values have correct data types."""
        ct = ControlTowerV3()
        stats = ct.get_tier_stats()
        
        # Counts should be integers
        assert isinstance(stats["total"], int)
        assert isinstance(stats["tier1_count"], int)
        assert isinstance(stats["tier2_count"], int)
        assert isinstance(stats["tier3_count"], int)
        
        # Percentages should be floats
        assert isinstance(stats["distribution"]["tier1_pct"], (int, float))
        assert isinstance(stats["distribution"]["tier2_pct"], (int, float))
        assert isinstance(stats["distribution"]["tier3_pct"], (int, float))
    
    def test_reset_tier_stats(self):
        """Test that reset_tier_stats() clears statistics."""
        ct = ControlTowerV3()
        
        # Simulate some detections by manually updating router stats
        ct.tier_router.tier_stats["tier1"] = 10
        ct.tier_router.tier_stats["tier2"] = 5
        ct.tier_router.tier_stats["tier3"] = 2
        ct.tier_router.tier_stats["total"] = 17
        
        # Verify counts are non-zero
        stats_before = ct.get_tier_stats()
        assert stats_before["total"] == 17
        
        # Reset
        ct.reset_tier_stats()
        
        # Verify counts are zero
        stats_after = ct.get_tier_stats()
        assert stats_after["total"] == 0
        assert stats_after["tier1_count"] == 0
        assert stats_after["tier2_count"] == 0
        assert stats_after["tier3_count"] == 0


class TestControlTowerV3Detection:
    """Test ControlTowerV3 detection methods."""
    
    def test_evaluate_response_returns_result(self):
        """Test that evaluate_response() returns a DetectionResult."""
        ct = ControlTowerV3()
        result = ct.evaluate_response(
            llm_response="This is a test response",
            context={}
        )
        
        # Check result has required attributes
        assert hasattr(result, "action")
        assert hasattr(result, "tier_used")
        assert hasattr(result, "method")
        assert hasattr(result, "confidence")
        assert hasattr(result, "processing_time_ms")
        assert hasattr(result, "failure_class")
        assert hasattr(result, "severity")
        assert hasattr(result, "explanation")
    
    def test_evaluate_response_valid_tier(self):
        """Test that evaluate_response() returns valid tier number."""
        ct = ControlTowerV3()
        result = ct.evaluate_response(
            llm_response="Test response",
            context={}
        )
        
        assert result.tier_used in [1, 2, 3], f"Invalid tier: {result.tier_used}"
    
    def test_evaluate_response_valid_confidence(self):
        """Test that evaluate_response() returns valid confidence."""
        ct = ControlTowerV3()
        result = ct.evaluate_response(
            llm_response="Test response",
            context={}
        )
        
        assert 0.0 <= result.confidence <= 1.0, f"Invalid confidence: {result.confidence}"
    
    def test_evaluate_response_without_context(self):
        """Test that evaluate_response() works without context."""
        ct = ControlTowerV3()
        result = ct.evaluate_response(llm_response="Test response")
        
        assert result is not None
        assert hasattr(result, "action")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
