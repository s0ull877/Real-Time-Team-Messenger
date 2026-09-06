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
    """
    room = await room_service.create_room(
        owner_id = user_id,
        room_name = room_data.name
    )

    return RoomResponse.model_validate(room)


@router.get("", status_code=status.HTTP_200_OK)
async def get_rоoms(
    user_id: CurrentUserIdDep,
    room_service: RoomServiceDep
) -> list[RoomResponse] | list[None]:
    """
    """
    rooms = await room_service.get_rooms_by_member_id(
        member_id = user_id
    )

    return [RoomResponse.model_validate(room) for room in rooms]


@router.get("/owned", status_code=status.HTTP_200_OK)
async def get_owned_rоoms(
    user_id: CurrentUserIdDep,
    room_service: RoomServiceDep
) -> list[RoomResponse] | list[None]:
    """
    """
    rooms = await room_service.get_owned_rooms(
        owner_id = user_id
    )

    return [RoomResponse.model_validate(room) for room in rooms]

