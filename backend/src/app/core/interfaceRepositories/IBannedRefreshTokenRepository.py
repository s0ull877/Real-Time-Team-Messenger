from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import BannedRefreshToken


class IBannedRefreshTokenRepository(ABC):
    """
    Interface for the room repository.
    """

    @abstractmethod
    async def ban(self, jti: UUID) -> BannedRefreshToken:
        """
        Create a new banned refresh token.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def is_banned(self, jti: UUID) -> bool:
        """
        Check if a refresh token is banned.
        """
        raise NotImplementedError

    