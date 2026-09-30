"""
즐겨찾기(Favorite) 비즈니스 로직.

즐겨찾기를 등록하려면 from/to 단위가 모두 현재 사용자에게 보이는 단위여야 하고,
같은 분야여야 한다(그렇지 않은 조합을 즐겨찾기해봤자 변환이 불가능하므로).
조회/삭제는 본인 소유의 즐겨찾기만 가능하다.
"""

from app.dto.dtos import FavoriteDTO
from app.repositories.favorite_repository import FavoriteRepository
from app.services.unit_service import UnitService


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository, unit_service: UnitService):
        self.favorite_repository = favorite_repository
        self.unit_service = unit_service

    def add_favorite(self, current_user_id: int, from_unit_id: int, to_unit_id: int) -> FavoriteDTO:
        from_unit = self.unit_service.get_visible_unit(current_user_id, from_unit_id)
        to_unit = self.unit_service.get_visible_unit(current_user_id, to_unit_id)

        if from_unit.category != to_unit.category:
            raise ValueError("서로 다른 분야의 단위 조합은 즐겨찾기할 수 없습니다.")

        entity = self.favorite_repository.create(current_user_id, from_unit_id, to_unit_id)
        return FavoriteDTO(
            favorite_id=entity.favorite_id,
            user_id=entity.user_id,
            from_unit=from_unit,
            to_unit=to_unit,
        )

    def list_my_favorites(self, current_user_id: int) -> list[FavoriteDTO]:
        entities = self.favorite_repository.find_by_user(current_user_id)
        result = []
        for entity in entities:
            from_unit = self.unit_service.get_visible_unit(current_user_id, entity.from_unit_id)
            to_unit = self.unit_service.get_visible_unit(current_user_id, entity.to_unit_id)
            result.append(
                FavoriteDTO(
                    favorite_id=entity.favorite_id,
                    user_id=entity.user_id,
                    from_unit=from_unit,
                    to_unit=to_unit,
                )
            )
        return result

    def delete_favorite(self, current_user_id: int, favorite_id: int) -> None:
        entity = self.favorite_repository.find_by_id(favorite_id)
        if entity is None:
            raise ValueError(f"즐겨찾기를 찾을 수 없습니다: favorite_id={favorite_id}")
        if entity.user_id != current_user_id:
            raise ValueError("본인의 즐겨찾기만 삭제할 수 있습니다.")
        self.favorite_repository.delete(favorite_id)
