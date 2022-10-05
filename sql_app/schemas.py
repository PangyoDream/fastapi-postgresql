from calendar import month
from typing import List, Union

from pydantic import BaseModel

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