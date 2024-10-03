# fastapi 기본 임포트
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

# dummy_routes.py에서 라우트 가져오기
from dummy_routes import router as dummy_router
from status_routes import router as status_router

app = FastAPI()

# CORS 설정 추가 - 모든 도메인 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)


@app.get("/")
def read_root():
    return {"PLKIT": "DEV"}


# dummy 관련 라우트 추가
app.include_router(dummy_router, prefix="/dummy")
# status 관련 라우트 추가
app.include_router(status_router, prefix="/status")


@app.post("/image")
async def save_image(request: Request):
    contents = await request.body()
    with open("current.jpeg", "wb") as fp:
        fp.write(contents)

    return "image send finished"


@app.get("/image")
async def get_image(request: Request):
    image_path = "current.jpeg"
    return FileResponse(image_path)
