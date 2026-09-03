import jwt
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services import AuthService, EmailActionTokenService, MailService, TokenService, UserService
from app.core.ports import IPasswordHasher
from app.infrastructure.database import database, SQLAlchemyUnitOfWork
from app.infrastructure.repositories import (
    EmailActionTokenRepository,
    BannedRefreshTokenRepository,
)
from app.infrastructure.config import get_settings
from app.infrastructure.security import PasswordHasher

settings = get_settings()

SessionDep = Annotated[AsyncSession, Depends(database.get_db_session)]


def get_password_hasher() -> IPasswordHasher:
    return PasswordHasher()


PasswordHasherDep = Annotated[IPasswordHasher, Depends(get_password_hasher)]


def get_mail_service(request: Request) -> MailService:
    kafka_producer = request.app.state.producer

    return MailService(
        broker_producer=kafka_producer,
    )


def get_user_service(
    password_hasher: PasswordHasherDep,
) -> UserService:
    return UserService(
        unit_of_work_factory=lambda: SQLAlchemyUnitOfWork(
            database.session_factory
        ),
        password_hasher=password_hasher,
    )


def get_email_action_token_service(
    session: SessionDep,
) -> EmailActionTokenService:
    email_action_token_repository = EmailActionTokenRepository(session=session)
    return EmailActionTokenService(repository=email_action_token_repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
EmailActionTokenServiceDep = Annotated[
    EmailActionTokenService,
    Depends(get_email_action_token_service),
]
MailServiceDep = Annotated[MailService, Depends(get_mail_service)]


async def get_token_service(
    session: SessionDep,
    user_service: UserServiceDep,
) -> TokenService:
    banned_refresh_token_repository = BannedRefreshTokenRepository(session=session)
    return TokenService(
        user_service=user_service,
        repository=banned_refresh_token_repository,
    )


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]


async def get_auth_service(
    email_action_service: EmailActionTokenServiceDep,
    token_service: TokenServiceDep,
    user_service: UserServiceDep,
    mail_service: MailServiceDep,
    password_hasher: PasswordHasherDep,
) -> AuthService:
    return AuthService(
        user_service=user_service,
        email_action_service=email_action_service,
        mail_service=mail_service,
        token_service=token_service,
        password_hasher=password_hasher,
    )


class JWTBearer:

    async def __call__(self, request: Request):

        credentials = request.cookies.get("access_token")

        if credentials:

            try:
                payload = jwt.decode(
                    credentials, settings.secret_key, algorithms=[settings.algorithm]
                )
                request.state.payload = payload
                return payload
            
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                )
            
        else:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No credentials provided"
            )
