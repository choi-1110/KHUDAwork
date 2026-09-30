"""서비스 계층 DTO -> 라우터 계층 응답 스키마 변환. 라우터 계층 소속(응답 형식 조립)."""

from app.dto.dtos import UnitDTO
from app.schemas.schemas import UnitResponse


def unit_dto_to_response(dto: UnitDTO, current_user_id: int) -> UnitResponse:
    return UnitResponse(
        unit_id=dto.unit_id,
        unit_name=dto.unit_name,
        category=dto.category,
        conversion_factor=dto.conversion_factor,
        is_mine=(dto.owner_id == current_user_id),
    )
