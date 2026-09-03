from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.core.interfaceRepositories import IUserRepository


class IPasswordHasher(ABC):
    @abstractmethod
    async def hash(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify(self, password: str, password_hash: str) -> bool:
        raise NotImplementedError


class IUnitOfWork(ABC):
    users: IUserRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
