

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:
    id: int
    username: str
    password: str


@dataclass
class UnitEntity:
    unit_id: int
    unit_name: str
    category: str
    conversion_factor: float
    user_id: Optional[int]  # None이면 시스템 기본 단위


@dataclass
class FavoriteEntity:
    favorite_id: int
    user_id: int
    from_unit_id: int
    to_unit_id: int
