"""
User 테이블 접근 담당. SQL과 sqlite3 사용법을 아는 유일한 계층.
"""

import sqlite3
from typing import Optional

from app.entities.entities import UserEntity


def _to_entity(row: sqlite3.Row) -> UserEntity:
    return UserEntity(id=row["id"], username=row["username"], password=row["password"])


class UserRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create(self, username: str, password: str) -> UserEntity:
        cursor = self.conn.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, password),
        )
        self.conn.commit()
        return UserEntity(id=cursor.lastrowid, username=username, password=password)

    def find_by_username(self, username: str) -> Optional[UserEntity]:
        row = self.conn.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        return _to_entity(row) if row else None

    def find_by_id(self, user_id: int) -> Optional[UserEntity]:
        row = self.conn.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        return _to_entity(row) if row else None
