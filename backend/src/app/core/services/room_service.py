from uuid import UUID
from dataclasses import dataclass

from app.core.interfaceRepositories import IRoomMemberRepository, IRoomRepository
from app.core.exceptions import AppError, NotFoundError, PermissionError
from app.core.ports import ITransaction

from app.core.entities import Room, RoomMember

@dataclass
class RoomService:

    room_repository: IRoomRepository
    room_member_repository: IRoomMemberRepository
    transaction: ITransaction

    async def _get_by_id(self, room_id: UUID) -> Room:

        room = await self.room_repository.get_by_id(room_id=room_id,)

        if not room:
            raise NotFoundError(
                f"Room with id:{room_id} does not exist"
            )

        return room
   

    async def create_room(self, owner_id: UUID, room_name: str) -> Room:

        room = await self.room_repository.create(
            room=Room(
                name=room_name,
                owner_id=owner_id
            )
        )

        await self.room_member_repository.add(
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
        )


    async def get_owned_rooms(self, owner_id: UUID) -> list[Room]:

        rooms = await self.room_repository.get_by_owner_id(owner_id=owner_id)

        return rooms


    async def get_rooms_by_member_id(self, member_id: UUID) -> list[Room]:

        rooms = await self.room_repository.get_by_member_id(member_id=member_id)

        return rooms


    async def update_room_name(self, room_id: UUID, user_id: UUID, name: str) -> Room:
        
        room = await self._get_by_id(room_id=room_id)

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

        room = await self._get_by_id(room_id=room_id)

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


    async def get_room_members(self, user_id: UUID, room_id: UUID) -> list[RoomMember]:

        room = await self._get_by_id(room_id=room_id)

        if not await self.room_member_repository.is_member(user_id=user_id, room_id=room_id):
            raise PermissionError(
                "User is not the room member"
            )

        return await self.room_member_repository.get_room_members(room_id=room_id)


    async def leave_room(self, user_id: UUID, room_id: UUID) -> None:

        room = await self._get_by_id(room_id=room_id)

        if not await self.room_member_repository.is_member(user_id=user_id, room_id=room_id):
            raise PermissionError(
                "User is not the room member"
            )

        if room.owner_id == user_id:
            raise AppError(
                message="The owner cannot leave the room. Delete it if it is no longer needed.",
                status_code=400
            )

        await self.room_member_repository.remove(
            room_member=RoomMember(
                user_id=user_id,
                room_id=room.id
        ))

        try:
            await self.transaction.commit()
        except Exception:
            await self.transaction.rollback()
            raise

        return


    async def can_send_invite(self, sender_id: UUID, recipient_id: UUID, room_id: UUID) -> Room:

        room = await self._get_by_id(room_id=room_id)

        if sender_id != room.owner_id:
            raise PermissionError(
                "Only the owner can invite people to the room."
            )

        if await self.room_member_repository.is_member(user_id=recipient_id, room_id=room_id):
            raise AppError(
                message=f"User with id:{recipient_id} already in room.",
                status_code=400
            )

        return room


    async def add_member(self, room_id: UUID, user_id: UUID) -> RoomMember:

        room = await self._get_by_id(room_id=room_id)

        room_member = await self.room_member_repository.add(
            room_member=RoomMember(
                room_id=room.id,
                user_id=user_id
            )
        )

        try:
            await self.transaction.commit()
        except Exception:
            await self.transaction.rollback()
            raise

        return room_member


    

