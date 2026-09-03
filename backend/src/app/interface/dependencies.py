import jwt
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


async def get_mail_service(request: Request):
    kafka_producer = request.app.state.producer

    yield MailService(
        broker_producer=kafka_producer,
    )


async def get_user_service(session: AsyncSession = Depends(database.get_db_session)):

    user_repository = UserRepository(session=session)
    yield UserService(repository=user_repository)


async def get_email_action_token_service(session: AsyncSession = Depends(database.get_db_session)):

    email_action_token_repository = EmailActionTokenRepository(session=session)
    yield EmailActionTokenService(repository=email_action_token_repository)


async def get_token_service(
        session: AsyncSession = Depends(database.get_db_session),
        user_service: UserService = Depends(get_user_service)
    ):

    banned_refresh_token_repository = BannedRefreshTokenRepository(session=session)
    yield TokenService(user_service=user_service, repository=banned_refresh_token_repository)


async def get_auth_service(
        email_action_token_service: EmailActionTokenService = Depends(get_email_action_token_service),
        token_service: TokenService = Depends(get_token_service),
        user_service: UserService = Depends(get_user_service),
        mail_service: MailService = Depends(get_mail_service),
    ):
    
    yield AuthService(
        user_service=user_service,
        email_action_token_service=email_action_token_service,
        mail_service=mail_service,
        token_service=token_service
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