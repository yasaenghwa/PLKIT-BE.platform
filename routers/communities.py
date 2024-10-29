# app/routers/communities.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, schemas
from database import get_db

router = APIRouter(prefix="/communities", tags=["Community"])

@router.post("/", response_model=schemas.community.CommunityResponse)
async def create_community(community: schemas.community.CommunityCreate, db: Session = Depends(get_db)):
    """
    새로운 커뮤니티 게시물을 생성합니다.
    """
    new_community = crud.community.create_community(db, community)
    return new_community

@router.get("/{community_id}", response_model=schemas.community.CommunityResponse)
async def get_community(community_id: int, db: Session = Depends(get_db)):
    """
    특정 커뮤니티 게시물의 상세 정보를 조회합니다.
    """
    community = crud.community.get_community(db, community_id)
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    return community

@router.delete("/{community_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_community(community_id: int, db: Session = Depends(get_db)):
    """
    특정 커뮤니티 게시물을 삭제합니다.
    """
    community = crud.community.delete_community(db, community_id)
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시물을 찾을 수 없습니다.")
    return

@router.get("/", response_model=List[schemas.community.CommunityResponse])
async def list_communities(keyword: Optional[str] = None, db: Session = Depends(get_db)):
    """
    모든 커뮤니티 게시물을 조회하거나 키워드로 필터링합니다.
    """
    communities = crud.community.list_communities(db, keyword)
    return communities
