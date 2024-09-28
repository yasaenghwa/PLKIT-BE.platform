# fastapi 기본 임포트
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

# dummy_routes.py에서 라우트 가져오기
from dummy_routes import router as dummy_router
from status_routes import router as status_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"PLKIT": "DEV"}

# dummy 관련 라우트 추가
app.include_router(dummy_router, prefix="/dummy")
# status 관련 라우트 추가
app.include_router(status_router, prefix="/status")