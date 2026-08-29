from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import RoomMember 


class IRoomMemberRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def add(self, user_id: UUID, room_id: UUID) -> RoomMember:
        """
        Add member in room.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def remove(self, user_id: UUID, room_id: UUID) -> RoomMember:
        """
        Remove member from room.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def is_member(self, user_id: UUID, room_id: UUID) -> bool:
        """
        return whether the user is a member of the group
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_room_members(self, room_id: UUID) -> list[RoomMember]:
        """
        Get room members
        """
        raise NotImplementedError
  