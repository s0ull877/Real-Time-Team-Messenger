from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import Message


class IMessageRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def create(self, message: Message) -> Message:
        """
        Create a new message.

        class Message:
            id: UUID | None = None
            room_id: UUID
            author_id: UUID
            encrypted_text: str
            deleted_at: datetime | None = None
            created_at: datetime
            updated_at: datetime
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_author_id_in_room(self, author_id: UUID, room_id: UUID) -> list[Message] | None:
        """
        Get user messages in current room.
        """
        raise NotImplementedError

    
    @abstractmethod
    async def update_encrypted_text(self, message_id: UUID, encrypted_text: str) -> Message:
        """
        Update message encrypted text.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, message_id: UUID) -> Message:
        """
        Soft deleting a message by modifying a field `deleted_at`.
        """
        raise NotImplementedError
