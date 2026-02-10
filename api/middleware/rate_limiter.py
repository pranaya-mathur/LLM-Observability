"""Rate limiting middleware."""

from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session


# In-memory rate limit store (replace with Redis in production)
rate_limit_store: Dict[str, Dict] = {}

# Rate limits per tier (requests per hour)
RATE_LIMITS = {
    "free": 100,
    "pro": 1000,
    "enterprise": 10000,
}


def get_rate_limit(tier: str) -> int:
    """Get rate limit for tier."""
    return RATE_LIMITS.get(tier, 100)


async def check_rate_limit(user, db: Session) -> dict:
    """Check if user has exceeded rate limit."""
    username = user.username
    tier = user.rate_limit_tier
    limit = get_rate_limit(tier)
    
    now = datetime.utcnow()
    
    # Initialize or get user's rate limit data
    if username not in rate_limit_store:
        rate_limit_store[username] = {
            "count": 0,
            "reset_at": now + timedelta(hours=1),
        }
    
    user_data = rate_limit_store[username]
    
    # Reset if window expired
    if now >= user_data["reset_at"]:
        user_data["count"] = 0
        user_data["reset_at"] = now + timedelta(hours=1)
    
    # Check limit
    if user_data["count"] >= limit:
        return {
            "allowed": False,
            "limit": limit,
            "remaining": 0,
            "reset_at": user_data["reset_at"].isoformat(),
        }
    
    # Increment counter
    user_data["count"] += 1
    
    return {
        "allowed": True,
        "limit": limit,
        "remaining": limit - user_data["count"],
        "reset_at": user_data["reset_at"].isoformat(),
    }


def reset_rate_limit(username: str):
    """Reset rate limit for user (admin function)."""
    if username in rate_limit_store:
        del rate_limit_store[username]


def get_rate_limit_info(username: str, tier: str) -> dict:
    """Get current rate limit info for user."""
    limit = get_rate_limit(tier)
    
    if username not in rate_limit_store:
        return {
            "limit": limit,
            "remaining": limit,
            "reset_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        }
    
    user_data = rate_limit_store[username]
    remaining = max(0, limit - user_data["count"])
    
    return {
        "limit": limit,
        "remaining": remaining,
        "reset_at": user_data["reset_at"].isoformat(),
    }
