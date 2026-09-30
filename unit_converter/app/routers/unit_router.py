"""
단위(Unit) 라우터. 로그인 필요 (Depends(get_current_user)).
로직은 최소화하고, 서비스 예외 -> HTTP 상태코드 변환만 담당한다.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_unit_service
from app.entities.entities import UserEntity
from app.routers.mappers import unit_dto_to_response
from app.schemas.schemas import UnitCreateRequest, UnitResponse
from app.services.unit_service import UnitService

router = APIRouter(prefix="/units", tags=["units"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_unit(
    request: UnitCreateRequest,
    current_user: UserEntity = Depends(get_current_user),
    unit_service: UnitService = Depends(get_unit_service),
) -> UnitResponse:
    try:
        dto = unit_service.create_unit(
            current_user.id, request.unit_name, request.category, request.conversion_factor
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return unit_dto_to_response(dto, current_user.id)


@router.get("")
def list_units(
    category: Optional[str] = None,
    current_user: UserEntity = Depends(get_current_user),
    unit_service: UnitService = Depends(get_unit_service),
) -> list[UnitResponse]:
    dtos = unit_service.list_visible_units(current_user.id, category)
    return [unit_dto_to_response(dto, current_user.id) for dto in dtos]


@router.get("/{unit_id}")
def get_unit(
    unit_id: int,
    current_user: UserEntity = Depends(get_current_user),
    unit_service: UnitService = Depends(get_unit_service),
) -> UnitResponse:
    try:
        dto = unit_service.get_visible_unit(current_user.id, unit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return unit_dto_to_response(dto, current_user.id)


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(
    unit_id: int,
    current_user: UserEntity = Depends(get_current_user),
    unit_service: UnitService = Depends(get_unit_service),
) -> None:
    try:
        unit_service.delete_unit(current_user.id, unit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
