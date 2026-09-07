from uuid import UUID
from dataclasses import dataclass

from app.core.interfaceRepositories import IRoomMemberRepository, IRoomRepository
from app.core.exceptions import NotFoundError, PermissionError
from app.core.ports import ITransaction

from app.core.entities import Room, RoomMember

@dataclass
class RoomService:

    room_repository: IRoomRepository
    room_member_repository: IRoomMemberRepository
    transaction: ITransaction

    async def create_room(self, owner_id: UUID, room_name: str) -> Room:

        room = await self.room_repository.create(
            room=Room(
                name=room_name,
                owner_id=owner_id
            )
        )

        members = await self.room_member_repository.add(
            room_member=RoomMember(
                room_id=room.id,
                user_id=room.owner_id
            )
        )
        
        try:
            await self.transaction.commit()
        except Exception:
            await self.transaction.rollback()
            raise

        return Room(
            id=room.id,
            name=room.name,
            owner_id=room.owner_id,
            members=[members]
        )


    async def get_owned_rooms(self, owner_id: UUID) -> list[Room] | list[None]:

        rooms = await self.room_repository.get_by_owner_id(owner_id=owner_id)

        return rooms


    async def get_rooms_by_member_id(self, member_id: UUID) -> list[Room] | list[None]:

        rooms = await self.room_repository.get_by_member_id(member_id=member_id)

        return rooms


    async def update_room_name(self, room_id: UUID, user_id: UUID, name: str) -> Room:
        
        room = await self.room_repository.get_by_id(room_id=room_id,)

        if not room:
            raise NotFoundError(
                f"Room with id:{room_id} does not exist"
            )

        if room.owner_id != user_id:
            raise PermissionError(
                "User is not the room owner"
            )

        if room.name == name:
            return room
        
        room.name = name

        updated_room = await self.room_repository.update_name_by_id(
            room_id=room.id,
            name=name
        )

        try:
            await self.transaction.commit()
        except Exception:
            await self.transaction.rollback()
            raise

        return updated_room


    async def delete_room(self, room_id: UUID, user_id: UUID) -> None:

        room = await self.room_repository.get_by_id(room_id=room_id,)

        if not room:
            raise NotFoundError(
                f"Room with id:{room_id} does not exist"
            )

        if room.owner_id != user_id:
            raise PermissionError(
                "User is not the room owner"
            )

        await self.room_repository.delete(room_id=room_id)

        try:
            await self.transaction.commit()
        except Exception:
            await self.transaction.rollback()
            raise

        return
    

