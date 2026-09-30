"""
Unit 테이블 접근 담당.

"다른 사용자에게 안 보이게" 하는 격리 로직의 첫 단계는 여기서 시작된다:
조회 쿼리 자체를 (user_id = 현재유저 OR user_id IS NULL) 로 필터링한다.
"""

import sqlite3
from typing import Optional

from app.entities.entities import UnitEntity


def _to_entity(row: sqlite3.Row) -> UnitEntity:
    return UnitEntity(
        unit_id=row["unit_id"],
        unit_name=row["unit_name"],
        category=row["category"],
        conversion_factor=row["conversion_factor"],
        user_id=row["user_id"],
    )


class UnitRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create(self, unit_name: str, category: str, conversion_factor: float, user_id: int) -> UnitEntity:
        cursor = self.conn.execute(
            "INSERT INTO unit (unit_name, category, conversion_factor, user_id) VALUES (?, ?, ?, ?)",
            (unit_name, category, conversion_factor, user_id),
        )
        self.conn.commit()
        return UnitEntity(
            unit_id=cursor.lastrowid,
            unit_name=unit_name,
            category=category,
            conversion_factor=conversion_factor,
            user_id=user_id,
        )

    def find_by_id(self, unit_id: int) -> Optional[UnitEntity]:
        row = self.conn.execute(
            "SELECT * FROM unit WHERE unit_id = ?", (unit_id,)
        ).fetchone()
        return _to_entity(row) if row else None

    def find_visible_to_user(self, user_id: int, category: Optional[str] = None) -> list[UnitEntity]:
        """시스템 기본 단위(user_id IS NULL) + 본인이 만든 단위만 조회."""
        query = "SELECT * FROM unit WHERE (user_id IS NULL OR user_id = ?)"
        params: list = [user_id]
        if category is not None:
            query += " AND category = ?"
            params.append(category)
        rows = self.conn.execute(query, params).fetchall()
        return [_to_entity(row) for row in rows]

    def delete(self, unit_id: int) -> None:
        self.conn.execute("DELETE FROM unit WHERE unit_id = ?", (unit_id,))
        self.conn.commit()

