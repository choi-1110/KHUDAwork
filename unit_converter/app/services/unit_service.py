"""
단위(Unit) 관련 비즈니스 로직.

핵심 규칙:
1. 조회 시 "시스템 기본 단위 OR 본인이 만든 단위"만 보여야 한다 (소유권 격리).
2. 삭제는 본인이 만든 단위만 가능하다 (기본 단위는 삭제 불가).
3. 기준 단위(factor=1.0)가 없는 새 분야를 만들 때를 제외하면, conversion_factor는
   사용자가 직접 입력한 값을 그대로 신뢰한다 (자동 계산 불가 — 논의 내용 반영).
"""

from typing import Optional

from app.dto.dtos import UnitDTO
from app.entities.entities import UnitEntity
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.unit_repository import UnitRepository


def _to_dto(entity: UnitEntity) -> UnitDTO:
    return UnitDTO(
        unit_id=entity.unit_id,
        unit_name=entity.unit_name,
        category=entity.category,
        conversion_factor=entity.conversion_factor,
        owner_id=entity.user_id,
    )


def _is_visible(entity: UnitEntity, current_user_id: int) -> bool:
    return entity.user_id is None or entity.user_id == current_user_id


class UnitService:
    def __init__(self, unit_repository: UnitRepository, favorite_repository: FavoriteRepository):
        self.unit_repository = unit_repository
        self.favorite_repository = favorite_repository

    def create_unit(
        self, current_user_id: int, unit_name: str, category: str, conversion_factor: float
    ) -> UnitDTO:
        if not unit_name or not category:
            raise ValueError("unit_name과 category는 비어 있을 수 없습니다.")
        if conversion_factor <= 0:
            raise ValueError("conversion_factor는 0보다 커야 합니다.")

        entity = self.unit_repository.create(unit_name, category, conversion_factor, current_user_id)
        return _to_dto(entity)

    def list_visible_units(self, current_user_id: int, category: Optional[str] = None) -> list[UnitDTO]:
        entities = self.unit_repository.find_visible_to_user(current_user_id, category)
        return [_to_dto(e) for e in entities]

    def get_visible_unit(self, current_user_id: int, unit_id: int) -> UnitDTO:
        """다른 사용자의 단위를 조회하려 하면 존재 여부와 무관하게 NotFound로 감춘다."""
        entity = self.unit_repository.find_by_id(unit_id)
        if entity is None or not _is_visible(entity, current_user_id):
            raise ValueError(f"단위를 찾을 수 없습니다: unit_id={unit_id}")
        return _to_dto(entity)

    def delete_unit(self, current_user_id: int, unit_id: int) -> None:
        entity = self.unit_repository.find_by_id(unit_id)
        if entity is None or not _is_visible(entity, current_user_id):
            raise ValueError(f"단위를 찾을 수 없습니다: unit_id={unit_id}")
        if entity.user_id is None:
            raise ValueError("기본 제공 단위는 삭제할 수 없습니다.")
        if self.favorite_repository.exists_referencing_unit(unit_id):
            raise ValueError("이 단위를 참조하는 즐겨찾기가 있어 삭제할 수 없습니다.")
        self.unit_repository.delete(unit_id)
