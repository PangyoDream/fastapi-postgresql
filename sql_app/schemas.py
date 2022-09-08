from calendar import month
from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    gender: str
    year: str
    month: str
    day: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Saju(BaseModel):
    gender: str
    year: str
    month: str
    day: str
    look: str
    personality: str