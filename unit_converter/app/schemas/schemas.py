
from typing import Optional

from pydantic import BaseModel, Field


# ---- Auth ----
class RegisterRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: int
    username: str


# ---- Unit ----
class UnitCreateRequest(BaseModel):
    unit_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    conversion_factor: float = Field(gt=0, description="해당 분야 기준 단위(factor=1.0) 대비 배수")


class UnitResponse(BaseModel):
    unit_id: int
    unit_name: str
    category: str
    conversion_factor: float
    is_mine: bool  # 기본 제공 단위(False)인지 내가 만든 단위(True)인지


# ---- Convert ----
class ConvertResponse(BaseModel):
    value: float
    from_unit: UnitResponse
    to_unit: UnitResponse
    result: float


# ---- Favorite ----
class FavoriteCreateRequest(BaseModel):
    from_unit_id: int
    to_unit_id: int


class FavoriteResponse(BaseModel):
    favorite_id: int
    from_unit: UnitResponse
    to_unit: UnitResponse
