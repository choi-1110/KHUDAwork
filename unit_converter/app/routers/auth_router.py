"""
회원가입/로그인 라우터. 다른 엔드포인트들은 요청마다 username, password
쿼리 매개변수로 로그인 여부를 검증한다 (get_current_user 참고).
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_auth_service, get_current_user
from app.entities.entities import UserEntity
from app.schemas.schemas import RegisterRequest, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> UserResponse:
    try:
        user = auth_service.register(request.username, request.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserResponse(id=user.id, username=user.username)


@router.get("/login")
def login(current_user: UserEntity = Depends(get_current_user)) -> UserResponse:
    """아이디/비밀번호가 맞으면 사용자 정보를, 틀리면 401을 반환한다."""
    return UserResponse(id=current_user.id, username=current_user.username)
