from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Set, Optional

from models.base import Base
from utils.time import get_morning_time


@dataclass
class Report(Base):
    """
    Represents a daily Instagram follower/following report.
    Stores user data and analysis results of changes between reports.
    """
    # Basic report data
    _id: str = ""
    generated_at: datetime = field(default_factory=get_morning_time)
    num_followers: int = 0
    num_following: int = 0
    users: List[Dict[str, Any]] = field(default_factory=list)

    # Analysis results - differences from a previous report
    new_followers: List[str] = field(default_factory=list)
    lost_followers: List[str] = field(default_factory=list)
    new_following: List[str] = field(default_factory=list)
    unfollowed: List[str] = field(default_factory=list)

    # Summary statistics
    stats: Dict[str, Any] = field(default_factory=dict)

    def get_users_by_type(self, user_type: str) -> List[Dict[str, Any]]:
        """Get all users of a specific type (follower, following, or both)."""
        return [user for user in self.users if user_type in user.get('type', [])]

    def get_user_ids_by_type(self, user_type: str) -> Set[str]:
        """Get all user IDs of a specific type."""
        return {user.get('_id') for user in self.get_users_by_type(user_type) if user.get('_id')}

    def get_mutual_users(self) -> List[Dict[str, Any]]:
        """Get users who both follow you and are followed by you."""
        return [user for user in self.users
                if 'follower' in user.get('type', []) and 'following' in user.get('type', [])]

    def get_non_mutual_followers(self) -> List[Dict[str, Any]]:
        """Get users who follow you, but you don't follow back."""
        return [user for user in self.users
                if 'follower' in user.get('type', []) and 'following' not in user.get('type', [])]

    def get_non_mutual_following(self) -> List[Dict[str, Any]]:
        """Get users who you follow but don't follow you back."""
        return [user for user in self.users
                if 'following' in user.get('type', []) and 'follower' not in user.get('type', [])]

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific user by ID."""
        for user in self.users:
            if str(user.get('_id')) == str(user_id):
                return user
        return None

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get a specific user by username."""
        for user in self.users:
            if user.get('username') == username:
                return user
        return None
