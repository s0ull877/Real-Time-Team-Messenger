from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.entities import User
from app.core.exceptions import NotFoundError, DuplicateEntryError
from app.core.interfaceRepositories import IUserRepository

from app.infrastructure.database.models import User as UserModel


class UserRepository(IUserRepository):
    """
    Interface for the user repository.
    """
    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, user_model: UserModel) -> User:
        """
        Convert a UserModel instance to a User entity.
        """
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password_hash=user_model.password_hash,
            avatar_url=user_model.avatar_url,
            is_verified=user_model.is_verified,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )


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

        Raises:
            IntegrityError: If a database integrity constraint is violated.
        """
        user_model = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            username=user.username,
            is_verified=user.is_verified,
            avatar_url=user.avatar_url,
        )

        self.session.add(user_model)

        try:
            await self.session.commit()
            await self.session.refresh(user_model)
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(user_model)
    

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Get a user by their ID.

        Returns:
            User entity if the user exists, otherwise None.
        """
        stmt = select(UserModel).where(UserModel.id == user_id)

        result = await self.session.execute(stmt)

        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return self._to_entity(user_model)


    async def get_by_email(self, email: str) -> User | None:
        """
        Get a user by their email address.

        Returns:
            User entity if the user exists, otherwise None.
        """
        stmt = select(UserModel).where(UserModel.email == email)

        result = await self.session.execute(stmt)

        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return self._to_entity(user_model)


    async def get_by_username(self, username: str) -> User | None:
        """
        Get a user by their username.

        Returns:
            User entity if the user exists, otherwise None.
        """
        stmt = select(UserModel).where(UserModel.username == username)

        result = await self.session.execute(stmt)

        user_model = result.scalar_one_or_none()

        if user_model is None:
            return None

        return self._to_entity(user_model)


    async def update(self, user: User) -> User:
        """
        Update an existing user's profile and account data.

        class User:
            id: UUID
            username: str
            email: str
            password_hash: str
            avatar_url: str | None
            is_verified: bool
            created_at: datetime
            updated_at: datetime 

        Raises:
            NotFoundError: If the user does not exist.
            IntegrityError: If a database integrity constraint is violated.
        """
        stmt = select(UserModel).where(UserModel.id == user.id)

        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            raise NotFoundError(
                f"User with id:{user.id} not found"
            )

        user_model.email = user.email
        user_model.username = user.username
        user_model.is_verified = user.is_verified
        user_model.avatar_url = user.avatar_url

        try:
            await self.session.commit()
            await self.session.refresh(user_model)
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(user_model)


    async def update_password_by_id(self, user_id: UUID, password_hash: str) -> User:
        """
        Update a user's password hash by their ID.

        Raises:
            NotFoundError: If the user does not exist.
            IntegrityError: If a database integrity constraint is violated.
        """
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(password_hash=password_hash)
            .returning(UserModel)
        )

        result = await self.session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model is None:
            await self.session.rollback()
            raise NotFoundError(
                f"User with id:{user_id} not found"
            )

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(user_model)


    async def delete(self, user_id: UUID) -> None:
        """
        Delete a user by id.

        Raise NotFoundError if the user does not exist.
        """
        stmt = delete(UserModel).where(UserModel.id == user_id)

        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundError(
                f"User with id:{user_id} not found"
            )

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise