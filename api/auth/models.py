"""Pydantic models for authentication."""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    username: str | None = None
    role: str | None = None


class UserBase(BaseModel):
    """Base user model."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserResponse(UserBase):
    """User response model."""
    role: str
    rate_limit_tier: str
    disabled: bool = False
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update model."""
    email: EmailStr | None = None
    role: str | None = None
    rate_limit_tier: str | None = None
    disabled: bool | None = None
