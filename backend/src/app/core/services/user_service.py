from dataclasses import dataclass
from collections.abc import Callable
from typing import NoReturn
from uuid import UUID

from app.core.entities import User
from app.core.interfaceRepositories import (
    CreateUserRepositoryDTO,
    UserAlreadyExistsRepositoryError,
)
from app.core.ports import IPasswordHasher, IUnitOfWork
from app.core.exceptions import (
    DuplicateEntryError,
    NotFoundError,
    ServiceError,
)
from .user_dto import CreateUserDTO


class UserAlreadyExistsError(ServiceError):
    def __init__(self, field: str, value: str) -> None:
        self.field = field
        self.value = value

        super().__init__(f"User with this {field} already exists")



@dataclass
class UserService:
    unit_of_work_factory: Callable[[], IUnitOfWork]
    password_hasher: IPasswordHasher

    @staticmethod
    def _raise_user_already_exists(
        exc: UserAlreadyExistsRepositoryError,
    ) -> NoReturn:
        raise UserAlreadyExistsError(
            field=exc.field,
            value=exc.value,
        ) from exc

    async def create(self, user: CreateUserDTO) -> User:
        """
        Create a new user.

        Raise UserAlreadyExistsError if the email or username already exists.
        """
        repository_user = CreateUserRepositoryDTO(
            username=user.username,
            email=user.email,
            password_hash=await self.password_hasher.hash(user.password),
        )
        async with self.unit_of_work_factory() as unit_of_work:
            try:
                created_user = await unit_of_work.users.create(repository_user)
            except UserAlreadyExistsRepositoryError as exc:
                self._raise_user_already_exists(exc)

            await unit_of_work.commit()
            return created_user


    async def get_by_id(self, user_id: UUID) -> User:
        """
        Get a user by id.
        If user does not exist raise NotFoundError.
        """
        
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            return user


    async def get_by_email(self, email: str) -> User:
        """
        Get a user by id.
        If user does not exist raise NotFoundError.
        """
        
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_email(email=email)
            if not user:
                raise NotFoundError(f"User with this email:{email} does not exist")

            return user


    async def update_profile_data(
            self, 
            user_id: UUID,
            username: str | None = None, 
            avatar_url: str | None = None
        ) -> User:

        """
        Update profile username/avatar_url.
        If user does not exist raise NotFoundError.
        """

        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            if username is not None:
                existing_user = await unit_of_work.users.get_by_username(
                    username=username
                )

                if existing_user and existing_user.id != user.id:
                    raise DuplicateEntryError(
                        msg=f"Username: {username} is busy",
                        duplicate_field={"username": username},
                    )

                user.username = username

            if avatar_url is not None:
                user.avatar_url = avatar_url

            try:
                updated_user = await unit_of_work.users.update(user=user)
            except UserAlreadyExistsRepositoryError as exc:
                self._raise_user_already_exists(exc)

            await unit_of_work.commit()
            return updated_user


    async def update_email(self, user_id: UUID,  email: str) -> User:
        """
        Update user email.

        If user does not exist, raise NotFoundError.
        If email belongs to another user, raise DuplicateEntryError.
        """
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            existing_user = await unit_of_work.users.get_by_email(email=email)
            if existing_user and existing_user.id != user.id:
                raise DuplicateEntryError(
                    msg=f"Email: {email} is busy",
                    duplicate_field={"email": email},
                )

            user.email = email

            try:
                updated_user = await unit_of_work.users.update(user=user)
            except UserAlreadyExistsRepositoryError as exc:
                self._raise_user_already_exists(exc)

            await unit_of_work.commit()
            return updated_user


    async def mark_as_verified(self, user_id: UUID) -> User:
        """
        Method for AuthService. Update user is_verified field.
        """
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            user.is_verified = True
            updated_user = await unit_of_work.users.update(user=user)
            await unit_of_work.commit()
            return updated_user


    async def delete(self, user_id: UUID) -> None:
        """
        Delete user.
        """
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            await unit_of_work.users.delete(user_id=user.id)
            await unit_of_work.commit()


    async def change_password(self, user_id: UUID, password: str) -> User:
        password_hash = await self.password_hasher.hash(password)
        async with self.unit_of_work_factory() as unit_of_work:
            user = await unit_of_work.users.get_by_id(user_id=user_id)
            if not user:
                raise NotFoundError(f"User with this id:{user_id} does not exist")

            updated_user = await unit_of_work.users.update_password_by_id(
                user_id=user.id,
                password_hash=password_hash,
            )
            await unit_of_work.commit()
            return updated_user
