from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud, schemas, database
from schemas.user import UserResponse
import jwt
from typing import Optional
from config import settings
from uuid import uuid4
from pathlib import Path

router = APIRouter(prefix="/users", tags=["Users"])

# OAuth2PasswordBearer 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 프로필 이미지 저장 경로 설정
UPLOAD_DIR = Path("uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 현재 사용자 검증 함수
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명을 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = crud.user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: schemas.user.UserResponse = Depends(get_current_user),
):
    """
    현재 로그인한 사용자의 정보를 반환합니다.
    """
    return current_user

@router.patch("/me/name", response_model=UserResponse)
async def update_user_name(
    name: Optional[str] = None,
    db: Session = Depends(database.get_db),
    current_user: schemas.user.UserResponse = Depends(get_current_user),
):
    """
    현재 로그인된 사용자의 이름을 업데이트합니다.
    - `name`: 새로운 이름
    """
    if name:
        update_data = {"name": name}
        updated_user = crud.user.update_user(db, user_id=current_user.id, update_data=update_data)
        return updated_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이름을 제공해야 합니다."
        )

@router.patch("/me/avatar", response_model=UserResponse)
async def update_user_avatar(
    avatar: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: schemas.user.UserResponse = Depends(get_current_user),
):
    """
    현재 로그인된 사용자의 프로필 이미지를 업데이트합니다.
    - `avatar`: 프로필 이미지 파일 업로드
    """
    # 프로필 이미지 업로드 및 저장
    avatar_filename = f"{uuid4()}{Path(avatar.filename).suffix}"
    avatar_path = UPLOAD_DIR / avatar_filename

    # 파일 저장
    with open(avatar_path, "wb") as buffer:
        buffer.write(avatar.file.read())
    
    # 기존 프로필 이미지 삭제 (옵션)
    if current_user.avatar:
        old_avatar_path = Path(current_user.avatar)
        if old_avatar_path.exists():
            old_avatar_path.unlink()

    # DB에 저장할 경로
    update_data = {"avatar": str(avatar_filename)}
    updated_user = crud.user.update_user(db, user_id=current_user.id, update_data=update_data)
    return updated_user

@router.get("/me/avatar", response_class=FileResponse)
async def get_user_avatar(
    current_user: schemas.user.UserResponse = Depends(get_current_user),
):
    """
    현재 로그인된 사용자의 프로필 이미지를 반환합니다.
    """
    if not current_user.avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="프로필 이미지가 설정되지 않았습니다."
        )
    
    avatar_path = UPLOAD_DIR / current_user.avatar
    if not avatar_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="프로필 이미지를 찾을 수 없습니다."
        )
    
    return FileResponse(avatar_path)

@router.get("/{id}/avatar", response_class=FileResponse)
async def get_user_avatar_by_id(
    id: int, db: Session = Depends(database.get_db)
):
    """
    특정 사용자의 프로필 이미지를 반환합니다.
    - `id`: 사용자 ID
    """
    
    # 사용자 조회
    user = crud.user.get_user_by_id(db, user_id=id)   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
        )

    # 프로필 이미지 경로 확인
    if not user.avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="프로필 이미지가 설정되지 않았습니다."
        )

    avatar_path = UPLOAD_DIR / user.avatar
    if not avatar_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="프로필 이미지를 찾을 수 없습니다."
        )

    return FileResponse(avatar_path)
