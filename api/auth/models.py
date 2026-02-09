"""Authentication data models."""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class RateLimitTier(str, Enum):
    """Rate limit tier enumeration."""
    FREE = "free"          # 100 req/hour
    PRO = "pro"            # 1000 req/hour
    ENTERPRISE = "enterprise"  # Custom limits


class User(BaseModel):
    """User base model."""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    rate_limit_tier: RateLimitTier = RateLimitTier.FREE
    disabled: bool = False


class UserCreate(BaseModel):
    """User creation model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserInDB(User):
    """User model with hashed password for database storage."""
    hashed_password: str
    created_at: Optional[str] = None
    last_login: Optional[str] = None


class Token(BaseModel):
    """JWT token response model."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    role: Optional[UserRole] = None


class APIKey(BaseModel):
    """API key model."""
    key_id: str
    name: str
    key: str
    user_id: str
    created_at: str
    last_used: Optional[str] = None