from dataclasses import dataclass
from uuid import UUID

from app.core.entities import User
from app.core.interfaceRepositories import IUserRepository
from app.core.exceptions import DuplicateEntryError, NotFoundError



@dataclass
class UserService:
    
    repository: IUserRepository

    async def create(self, user: User) -> User:
        """
        Create a new user.

        If user with current email or username already exist
        raise DuplicateEntryError with duplicate_field={'field_name': user.field}
        """
        if await self.repository.get_by_email(email=user.email):
            raise DuplicateEntryError(
                msg="User with this email already exists",
                duplicate_field={'email': user.email}
            )

        if await self.repository.get_by_username(username=user.username):
            raise DuplicateEntryError(
                msg="User with this username already exists",
                duplicate_field={'username': user.username}
            )

        return await self.repository.create(user)


    async def get_by_id(self, user_id: UUID) -> User:
        """
        Get a user by id.
        If user does not exist raise NotFoundError.
        """
        
        user = await self.repository.get_by_id(user_id=user_id)
        if not user:
            raise NotFoundError(f"User with this id:{user_id} does not exist")

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

        user = await self.get_by_id(user_id=user_id)

        if username is not None:
            existing_user = await self.repository.get_by_username(username=username)

            if existing_user and existing_user.id != user.id:

                # если на фронте не позволять вбивать тот же самый юзернейм то он нормально обработает ошибку
                raise DuplicateEntryError(
                    msg=f"Username: {username} is busy",
                    duplicate_field={"username": username},
                )

            user.username = username

        if avatar_url is not None:
            user.avatar_url = avatar_url

        return await self.repository.update(user=user)


    async def update_email(self, user_id: UUID,  email: str) -> User:
        """
        Update user email.

        If user does not exist, raise NotFoundError.
        If email belongs to another user, raise DuplicateEntryError.
        """
        user = await self.get_by_id(user_id=user_id)
        existing_user = await self.repository.get_by_email(email=email)

        if existing_user and existing_user.id != user.id:
            raise DuplicateEntryError(
                msg=f"Email: {email} is busy",
                duplicate_field={'email': email}
            )

        user.email = email

        return await self.repository.update(user=user)


    async def mark_as_verified(self, user: User) -> User:
        """
        Method for AuthService. Update user is_verified field.
        """
                
        user.is_verified = True

        return await self.repository.update(user=user)


    async def delete(self, user_id: UUID) -> None:
        """
        Delete user.
        """
        user = await self.get_by_id(user_id=user_id)
        await self.repository.delete(user_id=user.id)


    async def change_password_hash(self, user_id: UUID, password_hash: str) -> User:

        user = await self.get_by_id(user_id=user_id)
        return await self.repository.update_password_by_id(user_id=user.id, password_hash=password_hash)