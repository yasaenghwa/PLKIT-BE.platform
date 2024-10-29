# app/schemas/community.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommunityBase(BaseModel):
    title: str
    content: str
    image: Optional[str] = None

class CommunityCreate(CommunityBase):
    writer_id: int

class CommunityResponse(CommunityBase):
    id: int
    writer: dict
    created_at: datetime
    answers: List[dict] = []

    class Config:
        orm_mode = True
