# app/routers/markets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/markets", tags=["Market"])

@router.post("/", response_model=schemas.market.MarketResponse)
async def create_market(market: schemas.market.MarketCreate, db: Session = Depends(get_db)):
    """
    새로운 마켓 게시물을 생성합니다.
    """
    new_market = crud.market.create_market(db, market)
    return new_market

@router.get("/{market_id}", response_model=schemas.market.MarketResponse)
async def get_market(market_id: int, db: Session = Depends(get_db)):
    """
    특정 마켓 게시물의 상세 정보를 조회합니다.
    """
    market = crud.market.get_market(db, market_id)
    if not market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    return market

@router.delete("/{market_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_market(market_id: int, db: Session = Depends(get_db)):
    """
    특정 마켓 게시물을 삭제합니다.
    """
    market = crud.market.delete_market(db, market_id)
    if not market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    return

@router.get("/", response_model=List[schemas.market.MarketResponse])
async def list_markets(keyword: Optional[str] = None, db: Session = Depends(get_db)):
    """
    모든 마켓 게시물 목록을 조회하거나 검색어로 필터링합니다.
    """
    markets = crud.market.list_markets(db, keyword)
    return markets
