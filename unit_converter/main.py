"""
앱 진입점.

3계층(라우터/서비스/레포지토리)을 조립하기만 하고, 로직은 전혀 담지 않는다.
- 앱 생성 시 init_db()로 SQLite 테이블 생성 + 기본 단위 시딩
- 각 라우터를 include_router로 등록
"""

from fastapi import FastAPI

from app.database import init_db
from app.routers import auth_router, convert_router, favorite_router, unit_router

init_db()

app = FastAPI(title="단위 변환 & 즐겨찾기 서비스")


app.include_router(auth_router.router)
app.include_router(unit_router.router)
app.include_router(convert_router.router)
app.include_router(favorite_router.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
