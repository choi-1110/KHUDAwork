"""
단위 변환 비즈니스 로직.

1주차 과제의 핵심 아이디어(미터를 허브로 삼아 2단계로 변환)를 그대로 유지하되,
하드코딩된 TO_METER 딕셔너리 대신 DB에 저장된 Unit.conversion_factor를 사용하도록
일반화했다. from/to 단위는 반드시 현재 사용자에게 "보이는" 단위여야 하고,
같은 category(분야)에 속해야 한다.
"""

from app.dto.dtos import ConvertResultDTO
from app.services.unit_service import UnitService


class ConvertService:
    def __init__(self, unit_service: UnitService):
        self.unit_service = unit_service

    def convert(self, current_user_id: int, value: float, from_unit_id: int, to_unit_id: int) -> ConvertResultDTO:
        # get_visible_unit이 존재하지 않거나 다른 사용자 소유면 ValueError를 던진다.
        from_unit = self.unit_service.get_visible_unit(current_user_id, from_unit_id)
        to_unit = self.unit_service.get_visible_unit(current_user_id, to_unit_id)

        if from_unit.category != to_unit.category:
            raise ValueError(
                f"서로 다른 분야의 단위는 변환할 수 없습니다: {from_unit.category} != {to_unit.category}"
            )

        meters = value * from_unit.conversion_factor
        result = meters / to_unit.conversion_factor

        return ConvertResultDTO(
            value=value,
            from_unit=from_unit,
            to_unit=to_unit,
            result=round(result, 3),
        )
