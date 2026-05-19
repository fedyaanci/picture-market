from pydantic import BaseModel
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    is_artist: bool = False
    avatar_url: str | None = None
    balance: float = 0.0


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password_hash: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
