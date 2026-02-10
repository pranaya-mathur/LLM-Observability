"""Dependency injection for FastAPI."""

from functools import lru_cache
from dotenv import load_dotenv
from enforcement.control_tower_v3 import ControlTowerV3

# Load environment variables
load_dotenv()


@lru_cache()
def get_control_tower() -> ControlTowerV3:
    """Get singleton instance of Control Tower V3.
    
    This ensures we use a single instance across all requests,
    maintaining consistent statistics and caching.
    
    Tier 3 LLM agent is enabled. Requirements:
    - GROQ_API_KEY in .env (recommended - fast, free tier)
    - OR Ollama running locally: ollama serve && ollama run llama3.2
    
    If neither is available, Tier 3 will gracefully fallback to conservative allow.
    """
    return ControlTowerV3(enable_tier3=True)
