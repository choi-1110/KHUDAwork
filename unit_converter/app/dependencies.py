"""
FastAPI 의존성 주입 모음.

강의 노트의 Depends() 패턴을 그대로 따른다:
  get_database (예시) -> get_db (여기서는 sqlite3 커넥션)
그리고 이를 체이닝해서 레포지토리 -> 서비스 -> "현재 로그인 사용자"까지
라우터 함수 시그니처에 주입한다.
"""

import sqlite3

from fastapi import Depends, HTTPException, status

from app.database import get_connection
from app.entities.entities import UserEntity
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.unit_repository import UnitRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.convert_service import ConvertService
from app.services.favorite_service import FavoriteService
from app.services.unit_service import UnitService

def get_db() -> sqlite3.Connection:
    """요청 하나당 커넥션 하나."""
    conn = get_connection()
    return conn


# ---- 레포지토리 ----
def get_user_repository(conn: sqlite3.Connection = Depends(get_db)) -> UserRepository:
    return UserRepository(conn)


def get_unit_repository(conn: sqlite3.Connection = Depends(get_db)) -> UnitRepository:
    return UnitRepository(conn)


def get_favorite_repository(conn: sqlite3.Connection = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepository(conn)


# ---- 서비스 ----
def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)


def get_unit_service(
    unit_repo: UnitRepository = Depends(get_unit_repository),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository),
) -> UnitService:
    return UnitService(unit_repo, favorite_repo)


def get_convert_service(unit_service: UnitService = Depends(get_unit_service)) -> ConvertService:
    return ConvertService(unit_service)


def get_favorite_service(
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository),
    unit_service: UnitService = Depends(get_unit_service),
) -> FavoriteService:
    return FavoriteService(favorite_repo, unit_service)


# ---- 현재 로그인 사용자 ----
def get_current_user(
    username: str,
    password: str,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserEntity:
    """
    요청마다 쿼리 매개변수로 받은 아이디/비밀번호를 auth_service.authenticate로
    검증한다. 이 디펜더블을 주입받는 모든 엔드포인트에 username, password
    쿼리 매개변수가 자동으로 추가된다. 실패 시 401을 반환한다.
    """
    try:
        return auth_service.authenticate(username, password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
