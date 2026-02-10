"""User repository for database operations."""

from typing import Optional, List
from sqlalchemy.orm import Session
from persistence.models import User


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: dict) -> User:
        """Create a new user."""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all(self) -> List[User]:
        """Get all users."""
        return self.db.query(User).all()
    
    def update(self, username: str, user_data: dict) -> Optional[User]:
        """Update user."""
        user = self.get_by_username(username)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, username: str) -> bool:
        """Delete user."""
        user = self.get_by_username(username)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def update_role(self, username: str, role: str) -> Optional[User]:
        """Update user role."""
        return self.update(username, {"role": role})
    
    def update_tier(self, username: str, tier: str) -> Optional[User]:
        """Update user rate limit tier."""
        return self.update(username, {"rate_limit_tier": tier})
    
    def disable_user(self, username: str) -> Optional[User]:
        """Disable user account."""
        return self.update(username, {"disabled": True})
    
    def enable_user(self, username: str) -> Optional[User]:
        """Enable user account."""
        return self.update(username, {"disabled": False})
