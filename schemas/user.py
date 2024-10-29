# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    avatar: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str  # 변경된 필드명
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
