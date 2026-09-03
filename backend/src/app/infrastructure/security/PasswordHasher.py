import asyncio

from passlib.context import CryptContext

from app.core.ports import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    def __init__(self) -> None:
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash(self, password: str) -> str:
        return await asyncio.to_thread(self._context.hash, password)

    async def verify(self, password: str, password_hash: str) -> bool:
        return await asyncio.to_thread(
            self._context.verify,
            password,
            password_hash,
        )
