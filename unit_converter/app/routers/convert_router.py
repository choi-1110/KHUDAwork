"""
변환(Convert) 라우터. 1주차 GET /convert/length 를 계승하되, 하드코딩된 4개
단위 대신 DB에 등록된(시스템 + 내 소유) 단위를 unit_id로 지정해서 변환한다.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_convert_service, get_current_user
from app.entities.entities import UserEntity
from app.routers.mappers import unit_dto_to_response
from app.schemas.schemas import ConvertResponse
from app.services.convert_service import ConvertService

router = APIRouter(prefix="/convert", tags=["convert"])


@router.get("")
def convert(
    value: float,
    from_unit_id: int,
    to_unit_id: int,
    current_user: UserEntity = Depends(get_current_user),
    convert_service: ConvertService = Depends(get_convert_service),
) -> ConvertResponse:
    try:
        result = convert_service.convert(current_user.id, value, from_unit_id, to_unit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ConvertResponse(
        value=result.value,
        from_unit=unit_dto_to_response(result.from_unit, current_user.id),
        to_unit=unit_dto_to_response(result.to_unit, current_user.id),
        result=result.result,
    )
