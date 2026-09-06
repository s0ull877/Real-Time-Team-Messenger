from fastapi import APIRouter, status

from app.interface.dependencies import CurrentUserIdDep, RoomServiceDep
from app.interface.schemas import CreateRoom, RoomResponse


router = APIRouter(prefix="/rooms", tags=["user"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(
    user_id: CurrentUserIdDep,
    room_data: CreateRoom,
    room_service: RoomServiceDep
) -> RoomResponse:
    """
    Get user profile information by username
    If username == current user return full information
    """
    room = await room_service.create_room(
        owner_id = user_id,
        room_name = room_data.name
    )

    return RoomResponse.model_validate(room)