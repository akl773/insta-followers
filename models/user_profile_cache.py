from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, UTC
from typing import Optional, Dict
from pymongo import ASCENDING
from db_manager import get_db

@dataclass
class UserProfileCache:
    id: str
    username: str
    full_name: str
    profile_pic_url: str
    biography: Optional[str]
    website: Optional[str]
    is_private: bool
    is_verified: bool
    followers_count: int
    following_count: int
    media_count: int
    expire_at: datetime = field(default_factory=lambda: datetime.now(UTC) + timedelta(days=10))

    COLLECTION = 'user_profile_cache'

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfileCache':
        expire_at = data.get('expire_at', datetime.now(UTC) + timedelta(days=10))
        # Ensure expire_at is always offset-aware
        if isinstance(expire_at, datetime):
            if expire_at.tzinfo is None:
                expire_at = expire_at.replace(tzinfo=UTC)
        return cls(
            id=str(data.get('id', '')),
            username=data.get('username', ''),
            full_name=data.get('full_name', ''),
            profile_pic_url=data.get('profile_pic_url', ''),
            biography=data.get('biography'),
            website=data.get('website'),
            is_private=bool(data.get('is_private', False)),
            is_verified=bool(data.get('is_verified', False)),
            followers_count=int(data.get('followers_count', 0)),
            following_count=int(data.get('following_count', 0)),
            media_count=int(data.get('media_count', 0)),
            expire_at=expire_at
        )

    def to_dict(self) -> Dict:
        d = asdict(self)
        return d

    @classmethod
    def find_by_username(cls, username: str) -> Optional['UserProfileCache']:
        db = get_db()
        doc = db[cls.COLLECTION].find_one({"username": username})
        return cls.from_dict(doc) if doc else None

    @classmethod
    def upsert(cls, username: str, profile_data: Dict, ttl_days: int = 10) -> 'UserProfileCache':
        db = get_db()
        expire_at = datetime.now(UTC) + timedelta(days=ttl_days)
        cache = cls(
            id=str(profile_data.get('id', '')),
            username=username,
            full_name=profile_data.get('full_name', ''),
            profile_pic_url=profile_data.get('profile_pic_url', ''),
            biography=profile_data.get('biography'),
            website=profile_data.get('website'),
            is_private=bool(profile_data.get('is_private', False)),
            is_verified=bool(profile_data.get('is_verified', False)),
            followers_count=int(profile_data.get('followers_count', 0)),
            following_count=int(profile_data.get('following_count', 0)),
            media_count=int(profile_data.get('media_count', 0)),
            expire_at=expire_at
        )
        db[cls.COLLECTION].update_one(
            {"username": username},
            {"$set": cache.to_dict()},
            upsert=True
        )
        return cache

    @classmethod
    def ensure_ttl_index(cls):
        db = get_db()
        db[cls.COLLECTION].create_index(
            [("expire_at", ASCENDING)],
            expireAfterSeconds=0
        )

    def is_expired(self) -> bool:
        return self.expire_at < datetime.now(UTC)

    def get_dict(self) -> Dict:
        return self.to_dict()
