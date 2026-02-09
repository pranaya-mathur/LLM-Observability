"""User repository for managing user data."""

from typing import Optional, Dict, List
from datetime import datetime
import json
import os
from pathlib import Path

from api.auth.models import User, UserInDB, UserCreate, UserRole, RateLimitTier
from api.auth.jwt_handler import get_password_hash, verify_password


class UserRepository:
    """Repository for user data management.
    
    Uses JSON file storage for simplicity. In production, use PostgreSQL/MongoDB.
    """
    
    def __init__(self, storage_path: str = "data/users.json"):
        """Initialize user repository.
        
        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self) -> None:
        """Ensure storage directory and file exist."""
        storage_dir = Path(self.storage_path).parent
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists(self.storage_path):
            # Create with default admin user
            default_users = {
                "admin": {
                    "username": "admin",
                    "email": "admin@example.com",
                    "full_name": "System Administrator",
                    "role": "admin",
                    "rate_limit_tier": "enterprise",
                    "disabled": False,
                    "hashed_password": get_password_hash("admin123"),
                    "created_at": datetime.utcnow().isoformat(),
                    "last_login": None
                }
            }
            self._save_users(default_users)
    
    def _load_users(self) -> Dict[str, dict]:
        """Load users from storage."""
        with open(self.storage_path, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users: Dict[str, dict]) -> None:
        """Save users to storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(users, f, indent=2)
    
    def create_user(self, user_create: UserCreate) -> UserInDB:
        """Create a new user.
        
        Args:
            user_create: User creation data
            
        Returns:
            Created user with hashed password
            
        Raises:
            ValueError: If username already exists
        """
        users = self._load_users()
        
        if user_create.username in users:
            raise ValueError(f"Username '{user_create.username}' already exists")
        
        user_dict = {
            "username": user_create.username,
            "email": user_create.email,
            "full_name": user_create.full_name,
            "role": UserRole.USER.value,
            "rate_limit_tier": RateLimitTier.FREE.value,
            "disabled": False,
            "hashed_password": get_password_hash(user_create.password),
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None
        }
        
        users[user_create.username] = user_dict
        self._save_users(users)
        
        return UserInDB(**user_dict)
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username.
        
        Args:
            username: Username to lookup
            
        Returns:
            User if found, None otherwise
        """
        users = self._load_users()
        user_dict = users.get(username)
        
        if user_dict is None:
            return None
        
        return User(**user_dict)
    
    def get_user_with_password(self, username: str) -> Optional[UserInDB]:
        """Get user with hashed password for authentication.
        
        Args:
            username: Username to lookup
            
        Returns:
            User with password if found, None otherwise
        """
        users = self._load_users()
        user_dict = users.get(username)
        
        if user_dict is None:
            return None
        
        return UserInDB(**user_dict)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User if authentication successful, None otherwise
        """
        user = self.get_user_with_password(username)
        
        if user is None:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        self.update_last_login(username)
        
        return User(**user.dict())
    
    def update_last_login(self, username: str) -> None:
        """Update user's last login timestamp.
        
        Args:
            username: Username to update
        """
        users = self._load_users()
        
        if username in users:
            users[username]["last_login"] = datetime.utcnow().isoformat()
            self._save_users(users)
    
    def update_user_role(self, username: str, role: UserRole) -> Optional[User]:
        """Update user role.
        
        Args:
            username: Username to update
            role: New role
            
        Returns:
            Updated user if found, None otherwise
        """
        users = self._load_users()
        
        if username not in users:
            return None
        
        users[username]["role"] = role.value
        self._save_users(users)
        
        return User(**users[username])
    
    def update_rate_limit_tier(self, username: str, tier: RateLimitTier) -> Optional[User]:
        """Update user rate limit tier.
        
        Args:
            username: Username to update
            tier: New rate limit tier
            
        Returns:
            Updated user if found, None otherwise
        """
        users = self._load_users()
        
        if username not in users:
            return None
        
        users[username]["rate_limit_tier"] = tier.value
        self._save_users(users)
        
        return User(**users[username])
    
    def list_users(self) -> List[User]:
        """List all users.
        
        Returns:
            List of all users
        """
        users = self._load_users()
        return [User(**user_dict) for user_dict in users.values()]
    
    def disable_user(self, username: str) -> Optional[User]:
        """Disable a user account.
        
        Args:
            username: Username to disable
            
        Returns:
            Updated user if found, None otherwise
        """
        users = self._load_users()
        
        if username not in users:
            return None
        
        users[username]["disabled"] = True
        self._save_users(users)
        
        return User(**users[username])