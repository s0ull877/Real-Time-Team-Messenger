from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import Room
from app.core.exceptions import NotFoundError
from app.core.interfaceRepositories import IRoomRepository

from app.infrastructure.database.models import Room as RoomModel, RoomMember as RoomMemberModel

class RoomRepository(IRoomRepository):

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, room_model: RoomModel) -> Room:

        return Room(
            id=room_model.id,
            name=room_model.name,
            owner_id=room_model.owner_id,
        )


    async def create(self, room: Room) -> Room:

        room_model = RoomModel(
            id=room.id,
            name=room.name,
            owner_id=room.owner_id
        )

        self.session.add(room_model)

        await self.session.flush()
        await self.session.refresh(room_model)

        return self._to_entity(room_model)

    
    async def get_by_id(self, room_id: UUID) -> Room:
        """
        Get a room by id.
        """
        stmt = select(RoomModel).where(RoomModel.id == room_id)

        result = await self.session.execute(stmt)

        room_model = result.scalar_one_or_none()

        if room_model is None:
            return None

        return self._to_entity(room_model)


    async def get_by_owner_id(self, owner_id: UUID) -> list[Room] | list[None]:
        """
        """
        stmt = select(RoomModel).where(RoomModel.owner_id == owner_id)
        result = await self.session.execute(stmt)
        rooms_models = result.scalars().all()

        return [self._to_entity(room) for room in rooms_models]


    
    async def get_by_member_id(self, member_id: UUID) -> list[Room] | list[None]:
        """
        Get rooms of which the user is a member.
        If no suited rooms return empty list
        """
        stmt = (
            select(RoomModel)
            .options(selectinload(RoomModel.members))
            .where(
                RoomModel.members.any(
                    RoomMemberModel.user_id == member_id
                )
            )
        )

        result = await self.session.execute(stmt)
        rooms = result.scalars().all()

        return [self._to_entity(room) for room in rooms]


    async def update_name_by_id(self, room_id: UUID, name: str) -> Room | None:

        stmt = (
                update(RoomModel)
                .where(RoomModel.id == room_id)
                .values(name=name)
                .returning(RoomModel)
            )
        result = await self.session.execute(stmt)
        room = result.scalar_one()

        await self.session.flush()

        return self._to_entity(room)

    
    async def delete(self, room_id: UUID) -> None:
        """
        Delete room.
        """
        stmt = delete(RoomModel).where(RoomModel.id == room_id)

        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundError(
                f"Room with id:{room_id} not found"
            )

        await self.session.flush()

        return



    

