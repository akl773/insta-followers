from dataclasses import dataclass

from models.base import Base


@dataclass
class User(Base):
    _id: str = ""
    username: str = ""
    full_name: str = ""
    profile_pic_url: str = ""
