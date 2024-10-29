# app/schemas/market.py
from pydantic import BaseModel
from typing import List, Optional

class MarketBase(BaseModel):
    title: str
    content: str
    crop: str
    price: int
    location: str
    farm_name: str
    cultivation_period: str
    hashtags: Optional[List[str]] = None
    image: Optional[str] = None

class MarketCreate(MarketBase):
    writer_id: int

class MarketResponse(MarketBase):
    id: int
    writer: dict

    class Config:
        orm_mode = True
