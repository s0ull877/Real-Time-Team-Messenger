from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import Room
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
            members=room_model.members
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
        return

    
    async def get_by_owner_id(self, owner_id: UUID) -> list[Room] | list[None]:
        """
        """
        stmt = select(RoomModel).where(RoomModel.owner_id == owner_id).options(selectinload(RoomModel.members))
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


    
    async def update(self, room: Room) -> Room | None:
        """
        Update an existing room.

        class Room:
            id: UUID | None = None
            name: str
            owner_id: UUID
            created_at: datetime
            updated_at: datetime
        """
        return

    
    async def delete(self, room_id: UUID) -> None:
        """
        Delete room.
        """
        return

    

