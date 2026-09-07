from typing import Annotated

from fastapi import Depends

from app.core.services import RoomService
from app.infrastructure.repositories import RoomRepository, RoomMemberRepository
from . import SQLAlchemyTransaction

from . import SessionDep

async def get_room_service(
    session: SessionDep,
):
    transaction = SQLAlchemyTransaction(session=session)
    room_repository = RoomRepository(session=session)
    room_member_repository = RoomMemberRepository(session=session)

    yield RoomService(
        transaction=transaction, 
        room_repository=room_repository,
        room_member_repository=room_member_repository
    )


RoomServiceDep = Annotated[
    RoomService,
    Depends(get_room_service)
]