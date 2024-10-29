# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, schemas, database
from schemas.user import Token, UserResponse, UserCreate
import jwt
from typing import Optional
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])

# OAuth2PasswordBearer는 토큰 URL을 필요로 합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# 현재 사용자 검증 함수
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """
    JWT 토큰을 통해 현재 사용자를 확인합니다.

    Args:
        token (str): 인증 헤더에서 전달된 JWT 토큰.
        db (Session): 데이터베이스 세션 종속성.

    Returns:
        User: 인증된 사용자의 User 객체.

    Raises:
        HTTPException: 토큰이 유효하지 않거나 사용자를 찾을 수 없는 경우 발생.
    """
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

    Args:
        current_user (UserResponse): 현재 로그인한 사용자 정보.

    Returns:
        UserResponse: 로그인된 사용자의 정보.

    Raises:
        HTTPException: 사용자를 찾을 수 없을 때 발생.
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
        )
    return current_user
