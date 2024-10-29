# app/crud/community.py
from sqlalchemy.orm import Session
from models.community import Community
from schemas.community import CommunityCreate
from typing import Optional

def create_community(db: Session, community_data: CommunityCreate):
    community = Community(**community_data.dict())
    db.add(community)
    db.commit()
    db.refresh(community)
    return community

def get_community(db: Session, community_id: int):
    return db.query(Community).filter(Community.id == community_id).first()

def delete_community(db: Session, community_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community:
        db.delete(community)
        db.commit()
    return community

def list_communities(db: Session, keyword: Optional[str] = None):
    query = db.query(Community)
    if keyword:
        query = query.filter(Community.title.contains(keyword))
    return query.all()
