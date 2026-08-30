from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import Room


class IRoomRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def create(self, room: Room) -> Room:
        """
        Create a new room.

        class Room:
            id: UUID | None = None
            name: str
            owner_id: UUID
            created_at: datetime
            updated_at: datetime
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, room_id: UUID) -> Room:
        """
        Get a room by id.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_owner_id(self, owner_id: UUID) -> list[Room]:
        """
        Get owned rooms.
        If no suited rooms return None
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_member_id(self, memeber_id: UUID) -> list[Room]:
        """
        Get rooms of which the user is a member.
        If no suited rooms return None
        """
        raise NotImplementedError
    
    @abstractmethod
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
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, room_id: UUID) -> None:
        """
        Delete room.
        """
        raise NotImplementedError
