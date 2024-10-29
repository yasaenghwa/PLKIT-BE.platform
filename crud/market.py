# app/crud/market.py
from sqlalchemy.orm import Session
from models.market import Market
from schemas.market import MarketCreate
from typing import Optional

def create_market(db: Session, market_data: MarketCreate):
    market = Market(**market_data.dict())
    db.add(market)
    db.commit()
    db.refresh(market)
    return market

def get_market(db: Session, market_id: int):
    return db.query(Market).filter(Market.id == market_id).first()

def delete_market(db: Session, market_id: int):
    market = db.query(Market).filter(Market.id == market_id).first()
    if market:
        db.delete(market)
        db.commit()
    return market

def list_markets(db: Session, keyword: Optional[str] = None):
    query = db.query(Market)
    if keyword:
        query = query.filter(Market.title.contains(keyword) | Market.content.contains(keyword))
    return query.all()
