"""Dependency injection for FastAPI."""

from functools import lru_cache
from enforcement.control_tower_v3 import ControlTowerV3


@lru_cache()
def get_control_tower() -> ControlTowerV3:
    """Get singleton instance of Control Tower V3.
    
    This ensures we use a single instance across all requests,
    maintaining consistent statistics and caching.
    
    Note: Tier 3 LLM agent is enabled. Make sure Ollama is running:
          ollama run llama3.2
    """
    return ControlTowerV3(enable_tier3=True)
