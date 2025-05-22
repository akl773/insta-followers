from dataclasses import dataclass, field
from datetime import datetime

from Models.base import Base
from utils.time import get_morning_time


@dataclass
class Report(Base):
    generated_at: datetime = field(default_factory=get_morning_time)
    num_followers: int = 0
    num_following: int = 0
    users: list[dict] = field(default_factory=list)
