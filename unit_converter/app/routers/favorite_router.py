"""즐겨찾기(Favorite) 라우터."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_favorite_service
from app.entities.entities import UserEntity
from app.routers.mappers import unit_dto_to_response
from app.schemas.schemas import FavoriteCreateRequest, FavoriteResponse
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])


def _to_response(dto, current_user_id: int) -> FavoriteResponse:
    return FavoriteResponse(
        favorite_id=dto.favorite_id,
        from_unit=unit_dto_to_response(dto.from_unit, current_user_id),
        to_unit=unit_dto_to_response(dto.to_unit, current_user_id),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def add_favorite(
    request: FavoriteCreateRequest,
    current_user: UserEntity = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:
    try:
        dto = favorite_service.add_favorite(current_user.id, request.from_unit_id, request.to_unit_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return _to_response(dto, current_user.id)


@router.get("")
def list_favorites(
    current_user: UserEntity = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> list[FavoriteResponse]:
    dtos = favorite_service.list_my_favorites(current_user.id)
    return [_to_response(dto, current_user.id) for dto in dtos]


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    current_user: UserEntity = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> None:
    try:
        favorite_service.delete_favorite(current_user.id, favorite_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
