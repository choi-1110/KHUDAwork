"""
Favorite 테이블 접근 담당.
"""

import sqlite3
from typing import Optional

from app.entities.entities import FavoriteEntity


def _to_entity(row: sqlite3.Row) -> FavoriteEntity:
    return FavoriteEntity(
        favorite_id=row["favorite_id"],
        user_id=row["user_id"],
        from_unit_id=row["from_unit_id"],
        to_unit_id=row["to_unit_id"],
    )


class FavoriteRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create(self, user_id: int, from_unit_id: int, to_unit_id: int) -> FavoriteEntity:
        cursor = self.conn.execute(
            "INSERT INTO favorite (user_id, from_unit_id, to_unit_id) VALUES (?, ?, ?)",
            (user_id, from_unit_id, to_unit_id),
        )
        self.conn.commit()
        return FavoriteEntity(
            favorite_id=cursor.lastrowid,
            user_id=user_id,
            from_unit_id=from_unit_id,
            to_unit_id=to_unit_id,
        )

    def find_by_id(self, favorite_id: int) -> Optional[FavoriteEntity]:
        row = self.conn.execute(
            "SELECT * FROM favorite WHERE favorite_id = ?", (favorite_id,)
        ).fetchone()
        return _to_entity(row) if row else None

    def find_by_user(self, user_id: int) -> list[FavoriteEntity]:
        rows = self.conn.execute(
            "SELECT * FROM favorite WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [_to_entity(row) for row in rows]

    def delete(self, favorite_id: int) -> None:
        self.conn.execute("DELETE FROM favorite WHERE favorite_id = ?", (favorite_id,))
        self.conn.commit()

    def exists_referencing_unit(self, unit_id: int) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM favorite WHERE from_unit_id = ? OR to_unit_id = ? LIMIT 1",
            (unit_id, unit_id),
        ).fetchone()
        return row is not None

