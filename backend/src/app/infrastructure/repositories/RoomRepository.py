from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import Room
from app.core.interfaceRepositories import IRoomRepository

from app.infrastructure.database.models import Room as RoomModel


class RoomRepository(IRoomRepository):

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, room_model: RoomModel) -> Room:

        return Room(
            id=room_model.id,
            name=room_model.name,
            owner_id=room_model.owner_id
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

    
    async def get_by_owner_id(self, owner_id: UUID) -> list[Room]:
        """
        Get owned rooms.
        If no suited rooms return None
        """
        return

    
    async def get_by_member_id(self, memeber_id: UUID) -> list[Room]:
        """
        Get rooms of which the user is a member.
        If no suited rooms return None
        """
        return

    
    async def update(self, room: Room) -> Room:
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

    

