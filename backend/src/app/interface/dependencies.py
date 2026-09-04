import jwt
from typing import Annotated 
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.services import AuthService, EmailActionTokenService, MailService, TokenService, UserService
from app.infrastructure.database import database
from app.infrastructure.repositories import (
    UserRepository,
    EmailActionTokenRepository,
    BannedRefreshTokenRepository,
)
from app.infrastructure.config import get_settings

settings = get_settings()

SessionDep = Annotated[
    AsyncSession,
    Depends(database.get_db_session),
]


def get_mail_service(request: Request) -> MailService:
    kafka_producer = request.app.state.producer

    return MailService(
        broker_producer=kafka_producer,
    )


MailServiceDep = Annotated[
    MailService,
    Depends(get_mail_service),
]


async def get_user_service(
    session: SessionDep,
):
    repository = UserRepository(session=session)

    yield UserService(repository=repository)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]


async def get_email_action_token_service(
    session: SessionDep,
):
    repository = EmailActionTokenRepository(session=session)

    yield EmailActionTokenService(repository=repository)


EmailActionTokenServiceDep = Annotated[
    EmailActionTokenService,
    Depends(get_email_action_token_service),
]


async def get_token_service(
    session: SessionDep,
    user_service: UserServiceDep,
):
    repository = BannedRefreshTokenRepository(session=session)

    yield TokenService(
        user_service=user_service,
        repository=repository,
    )


TokenServiceDep = Annotated[
    TokenService,
    Depends(get_token_service),
]


async def get_auth_service(
    email_action_token_service: EmailActionTokenServiceDep,
    token_service: TokenServiceDep,
    user_service: UserServiceDep,
    mail_service: MailServiceDep,
):
    yield AuthService(
        user_service=user_service,
        email_action_service=email_action_token_service,
        mail_service=mail_service,
        token_service=token_service,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


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