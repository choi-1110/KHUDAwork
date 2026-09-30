"""
회원가입/로그인 검증 로직.

"로그인 검증"이라는 비즈니스 규칙을 서비스 계층에 둠으로써, 라우터는
Depends를 통해 이 서비스만 호출하면 된다. 실패 시 HTTPException이 아닌
ValueError를 던지고, HTTP 상태코드 변환은 라우터 쪽에서 담당한다.
"""

from app.entities.entities import UserEntity
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username: str, password: str) -> UserEntity:
        if self.user_repository.find_by_username(username) is not None:
            raise ValueError(f"이미 사용 중인 아이디입니다: {username}")
        return self.user_repository.create(username, password)

    def authenticate(self, username: str, password: str) -> UserEntity:
        """username/password가 올바르면 UserEntity를, 아니면 ValueError를 발생시킨다."""
        user = self.user_repository.find_by_username(username)
        if user is None or user.password != password:
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")
        return user
