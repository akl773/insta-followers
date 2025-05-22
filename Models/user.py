from dataclasses import dataclass

from Models.base import Base


@dataclass
class User(Base):
    id: str = ""
    username: str = ""
    full_name: str = ""
    profile_pic_url: str = ""
