from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import EmailVerification


class IEmailVerificationRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def create(self, email_verification: EmailVerification) -> EmailVerification:
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
    async def get_by_token_hash(self, token_hash: str) -> EmailVerification | None:
        """
        Get email verification by hash.
        """
        raise NotImplementedError

    
    @abstractmethod
    async def mark_as_used(self, email_verification_id: UUID) -> EmailVerification:
        """
        Update email_verification field `used_at`.
        """
        raise NotImplementedError
    
  