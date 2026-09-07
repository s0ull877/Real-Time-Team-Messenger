from uuid import UUID

from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from app.core.entities import ActionEnum

from app.interface.dependencies import CurrentUserIdDep, RoomServiceDep, \
    UserServiceDep, MailServiceDep, EmailActionTokenServiceDep
from app.interface.schemas import CreateRoom, RoomResponse, UpdateRoom, \
    RoomMemberResponse, InviteRoom


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


@router.get("/{room_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_room(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    room_service: RoomServiceDep
) -> Response:

    await room_service.leave_room(user_id=user_id, room_id=room_id)


@router.post("/{room_id}/invite", status_code=status.HTTP_200_OK)
async def invite_user(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    invite_data: InviteRoom,
    room_service: RoomServiceDep,
    user_service: UserServiceDep,
    email_action_service: EmailActionTokenServiceDep,
    mail_service: MailServiceDep
) -> Response:

    recipient = await user_service.get_by_username(username=invite_data.username)

    if recipient.id == user_id:
        return

    room = await room_service.can_send_invite(sender_id=user_id, recipient_id=recipient.id, room_id=room_id)
    if room:

        user = await user_service.get_by_id(user_id=user_id)
        _, token = await email_action_service.create(email=recipient.email, action=ActionEnum.ROOM_INVITATION)
        await mail_service.send_room_invitation_token(
            to=recipient.email, 
            token=token, 
            sender_username=user.username, 
            room_id=room.id, 
            room_name=room.name
        )


@router.get("/{room_id}/accept/{token}", status_code=status.HTTP_200_OK)
async def accept_invitation(
    user_id: CurrentUserIdDep,
    room_id: UUID,
    token: str,
    room_service: RoomServiceDep,
    user_service: UserServiceDep,
    email_action_service: EmailActionTokenServiceDep
) -> RoomMemberResponse:

    email_verification = await email_action_service.get_without_verifying(token=token)
    user = await user_service.get_by_id(user_id=user_id)

    if user.email != email_verification.email:
        return JSONResponse(
            status_code=403,
            content={
                "message": "This link is for another user.",
                "details": {}
            },
        )

    room_member = await room_service.add_member(room_id=room_id, user_id=user_id)

    return RoomMemberResponse.model_validate(room_member)


