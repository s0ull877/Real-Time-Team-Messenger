from uuid import uuid4, UUID
from datetime import timedelta
from dataclasses import dataclass
from passlib.context import CryptContext

from app.core.entities import User, TokenPair, ActionEnum
from app.core.exceptions import NotFoundError, InvalidVerificationError, \
    InvalidCredentialsError, InvalidActionTokenError, DuplicateEntryError
from . import UserService, EmailActionTokenService, MailService, TokenService



@dataclass
class AuthService:

    user_service: UserService
    email_action_service: EmailActionTokenService
    mail_service: MailService
    token_service: TokenService
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def register(self, email: str, username: str, password: str) -> User:
        """
        Register a new user.

        Hash the password, create the user, create an email verification
        token, and send the verification email.

        Raise DuplicateEntryError if the email or username is already in use.

        Return the created user.
        """
        password_hash = self.pwd_context.hash(password)
        user = await self.user_service.create(
            user=User(
                    username=username,
                    email=email,
                    password_hash=password_hash
                )
        )

        _, token = await self.email_action_service.create(user_id=user.id, action=ActionEnum.VERIFY_EMAIL)
        await self.mail_service.send_verify_token(to=user.email, token=token)

        return user


    async def verify_email(self, token) -> User:
        """
        Verify a user's email address using an email action token.

        Raise InvalidVerificationError if the token is invalid, expired,
        or has already been used.

        Raise InvalidActionTokenError if the token is not intended
        for email verification.

        Mark the user's email as verified and return the updated user.
        """
        email_verification = await self.email_action_service.verify(token=token)

        if email_verification.action != ActionEnum.VERIFY_EMAIL:
            raise InvalidActionTokenError(
                "Invalid token action."
            )

        return await self.user_service.mark_as_verified(user_id=email_verification.user_id)


    async def login(self, email: str, password: str) -> TokenPair:
        """
        Authenticate a user using their email and password.

        Raise InvalidCredentialsError if the email does not exist
        or the password is incorrect.

        Raise InvalidVerificationError if the user's email is not verified.

        Return a new access and refresh token pair.
        """
        try:
            user = await self.user_service.get_by_email(email=email)
        except NotFoundError as exc:
            raise InvalidCredentialsError("Invalid email or password") from exc

        if not self.pwd_context.verify(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_verified:
            raise InvalidVerificationError(
                "User email is not verified! Check email!"
            )

        access_token = self.token_service.create_access_token(
            {"sub": str(user.id)}
        )

        refresh_token = self.token_service.create_refresh_token(
            {"sub": str(user.id), "jti": str(uuid4())}
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    async def logout(self, token: str) -> None:
        """
        Log out a user by invalidating their refresh token.

        The refresh token becomes unavailable for further use.
        """
        return await self.token_service.ban_refresh_token(token=token)


    async def refresh(self, token: str) -> TokenPair:
        """
        Rotate a refresh token and issue a new access and refresh token pair.

        Raise InvalidTokenError if the refresh token is invalid, expired,
        has an incorrect token type, or has already been invalidated.

        Return a new access and refresh token pair.
        """
        return await self.token_service.refresh(token=token)


    async def request_password_reset(self, email: str) -> None:
        """
        Create a password reset token and send it to the user's email.

        Raise NotFoundError if the user with the specified email does not exist.

        The generated token is valid for a limited period of time.
        """
        user = await self.user_service.get_by_email(
            email=email
        )

        _, token = await self.email_action_service.create(
            user_id=user.id,
            action=ActionEnum.RESET_PASSWORD,
            expires_in=timedelta(minutes=15),
        )

        await self.mail_service.send_reset_password_token(
            to=user.email,
            token=token,
        )


    async def reset_password(self, token: str, new_password: str) -> User:
        """
        Reset a user's password using a password reset token.

        Raise InvalidVerificationError if the token is invalid, expired,
        or has already been used.

        Raise InvalidActionTokenError if the token is not intended
        for password reset.

        Update the user's password hash and return the updated user.
        """
        email_action_token = await self.email_action_service.verify(
            token=token
        )

        if email_action_token.action != ActionEnum.RESET_PASSWORD:
            raise InvalidActionTokenError(
                "Invalid token action."
            )

        password_hash = self.pwd_context.hash(
            new_password,
        )


        #! нужно добавить инвалидацию всех рефреш токенов пользователя по user_id
        return await self.user_service.change_password_hash(
            user_id=email_action_token.user_id,
            password_hash=password_hash,
        )



    async def request_email_change( self, user_id: UUID, new_email: str) -> None:
        """
        Request an email address change for a user.

        Verify that the new email address is not already in use,
        create an email change token, and send the verification email
        to the new address.

        Raise DuplicateEntryError if the new email address is already in use.
        """
        try:

            await self.user_service.get_by_email(new_email)

        except NotFoundError:

            _, token = await self.email_action_service.create(
                user_id=user_id,
                action=ActionEnum.CHANGE_EMAIL,
                email=new_email
            )

            await self.mail_service.send_change_email_token(
                to=new_email,
                token=token
            )
            
        else:

            raise DuplicateEntryError(f"Email: {new_email} is busy")


    async def change_email(self, token: str) -> User:
        """
        Change a user's email address using a valid email change token.

        Verify the token and ensure that it is intended for email change.

        Raise InvalidVerificationError if the token is invalid, expired,
        or has already been used.

        Raise InvalidActionTokenError if the token is not intended
        for email change.

        Update the user's email address and return the updated user.
        """
        email_action = await self.email_action_service.verify(
            token=token
        )
        
        if email_action.action != ActionEnum.VERIFY_EMAIL:
            raise InvalidActionTokenError("Invalid token action.")
        
        return await self.user_service.update_email(
            user_id=email_action.user_id,
            email=email_action.email,
        )