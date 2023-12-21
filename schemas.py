from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    name: Optional[str] = None


class Group(GroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int



class UserBase(BaseModel):
    name: str
    group_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    group_id: Optional[int] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
