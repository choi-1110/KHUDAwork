"""
DTO(Data Transfer Object) 정의.

DTO는 오직 데이터 전달만 담당하며(setter/getter 외 메서드 없음), 서비스 계층의
비즈니스 로직을 반영해 정의한다. 라우터의 Pydantic 스키마나 레포지토리의
엔티티가 바뀌어도, 그 변경분을 라우터/레포지토리 호출부에서만 흡수하면
서비스 계층 함수 시그니처는 그대로 유지할 수 있다.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UnitDTO:
    """서비스가 반환하는 '단위 하나'의 데이터 전달용 객체."""
    unit_id: int
    unit_name: str
    category: str
    conversion_factor: float
    owner_id: Optional[int]


@dataclass
class ConvertResultDTO:
    value: float
    from_unit: UnitDTO
    to_unit: UnitDTO
    result: float


@dataclass
class FavoriteDTO:
    favorite_id: int
    user_id: int
    from_unit: UnitDTO
    to_unit: UnitDTO
