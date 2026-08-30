from uuid import UUID
from abc import ABC, abstractmethod

from app.core.entities import User


class IUserRepository(ABC):
    """
    Interface for the user repository.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user.

        class User:
            id: UUID
            username: str
            email: str
            password_hash: str
            avatar_url: str | None
            is_verified: bool
            created_at: datetime
            updated_at: datetime
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Get a user by id.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Get a user by email.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """
        Get a user by username.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update an existing user.

        class User:
            id: UUID
            username: str
            email: str
            password_hash: str
            avatar_url: str | None
            is_verified: bool
            created_at: datetime
            updated_at: datetime 


        UPD: для оптимизации запросов можно разделить метод на update password, email и просто обычные поля
        """
        raise NotImplementedError

    @abstractmethod
    async def update_password_by_id(self, user_id: UUID, password_hash: str) -> User:
        """
        Update password hash by user_id.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """
        Delete a user.
        """
        raise NotImplementedError
