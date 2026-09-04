from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    async def hash(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify(self, password: str, password_hash: str) -> bool:
        raise NotImplementedError


class ITransaction(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
