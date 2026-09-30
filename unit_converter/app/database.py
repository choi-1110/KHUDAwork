"""
DB 연결 관리 모듈.

- SQLite 파일 위치, 커넥션 생성, 테이블 생성(스키마)을 담당한다.
- 레포지토리 계층은 이 모듈이 제공하는 커넥션만 사용하고,
  SQL 실행 방식(sqlite3)이 바뀌어도 다른 계층은 영향을 받지 않는다.
"""

import sqlite3

DB_PATH = "app.db"  # 프로젝트 루트에서 실행하면 루트에 생성된다.


def get_connection() -> sqlite3.Connection:
    """요청마다 새 커넥션을 반환한다. Row를 dict처럼 다룰 수 있게 row_factory 설정."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """앱 시작 시 1회 호출. ERD에 정의된 3개 테이블을 생성하고 기본 단위를 시딩한다."""
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS unit (
                unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_name TEXT NOT NULL,
                category TEXT NOT NULL,
                conversion_factor REAL NOT NULL,
                user_id INTEGER NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );

            CREATE TABLE IF NOT EXISTS favorite (
                favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                from_unit_id INTEGER NOT NULL,
                to_unit_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (from_unit_id) REFERENCES unit(unit_id),
                FOREIGN KEY (to_unit_id) REFERENCES unit(unit_id)
            );
            """
        )
        # 1주차 과제의 기본 단위(길이)를 시스템 제공 단위로 시딩 (user_id = NULL)
        existing = conn.execute(
            "SELECT COUNT(*) FROM unit WHERE user_id IS NULL"
        ).fetchone()[0]
        if existing == 0:
            conn.executemany(
                "INSERT INTO unit (unit_name, category, conversion_factor, user_id) "
                "VALUES (?, ?, ?, NULL)",
                [
                    ("meter", "length", 1.0),
                    ("yard", "length", 0.9144),
                    ("inch", "length", 0.0254),
                    ("feet", "length", 0.3048),
                ],
            )
        conn.commit()
    finally:
        conn.close()
