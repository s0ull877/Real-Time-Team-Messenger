from datetime import datetime
from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import EmailActionToken, ActionEnum


class IEmailActionTokenRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def create(self, email_action: EmailActionToken) -> EmailActionToken:
        """
        Create a new email verification.

        class EmailVerification:
            id: UUID | None = None
            user_id: UUID
            token_hash: str
            expires_at: datetime
            used_at: datetime | None = None
            created_at: datetime
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> EmailActionToken | None:
        """
        Get email verification by hash.
        """
        raise NotImplementedError

    
    @abstractmethod
    async def mark_as_used(self, token_hash: str, used_at: datetime) -> EmailActionToken:
        """
        Update email_verification field `used_at`.
        """
        raise NotImplementedError
    

    @abstractmethod
    async def delete_by_email_and_action(self, user_id: UUID, action: ActionEnum) -> None:
        """
        Update email_verification field `used_at`.
        """
        raise NotImplementedError
    