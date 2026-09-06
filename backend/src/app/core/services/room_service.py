from uuid import UUID
from dataclasses import dataclass

from app.core.ports import ITransaction
from app.core.interfaceRepositories import IRoomMemberRepository, IRoomRepository

from app.core.entities import RoomServiceDTO, Room, RoomMember

@dataclass
class RoomService:

    room_repository: IRoomRepository
    room_member_repository: IRoomMemberRepository
    transaction: ITransaction

    async def create_room(self, owner_id: UUID, room_name: str) -> RoomServiceDTO:

        room = await self.room_repository.create(
            room=Room(
                name=room_name,
                owner_id=owner_id
            )
        )

        room_member = await self.room_member_repository.add(
            room_member=RoomMember(
                room_id=room.id,
                user_id=room.owner_id
            )
        )
        await self.transaction.commit()

        return RoomServiceDTO(
            id=room.id,
            name=room.name,
            owner_id=room.owner_id,
            room_members=[room_member]
        )