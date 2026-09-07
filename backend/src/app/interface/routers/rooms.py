from uuid import UUID

from fastapi import APIRouter, status, Response

from app.interface.dependencies import CurrentUserIdDep, RoomServiceDep
from app.interface.schemas import CreateRoom, RoomResponse, UpdateRoom, RoomMemberResponse


router = APIRouter(prefix="/rooms", tags=["rooms"])

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


@router.post("/{room_id}", status_code=status.HTTP_200_OK)
async def update_room(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    room_data: UpdateRoom,
    room_service: RoomServiceDep
) -> RoomResponse:
    """
    """
    updated_room = await room_service.update_room_name(
        user_id=user_id,
        room_id=room_id, 
        name=room_data.name
    )
    return RoomResponse.model_validate(updated_room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    room_service: RoomServiceDep
) -> Response:
    """
    """
    await room_service.delete_room(
        user_id=user_id,
        room_id=room_id
    )



@router.get("/{room_id}/members", status_code=status.HTTP_200_OK)
async def get_room_members(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    room_service: RoomServiceDep
) -> list[RoomMemberResponse]:
    """
    """
    room_members = await room_service.get_room_members(
        user_id=user_id,
        room_id=room_id
    )

    return [RoomMemberResponse.model_validate(room_member) for room_member in room_members]

