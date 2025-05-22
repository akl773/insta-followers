from dataclasses import dataclass, field
from datetime import datetime

from utils.time import get_morning_time


@dataclass
class Report:
    generated_at: datetime = field(default_factory=lambda: get_morning_time)
    num_followers: int = 0
    num_following: int = 0
    users: list[dict] = field(default_factory=list)
