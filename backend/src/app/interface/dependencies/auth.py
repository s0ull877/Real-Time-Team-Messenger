from typing import Annotated 
from app.infrastructure.database.transaction import SQLAlchemyTransaction
from fastapi import Depends

from app.core.services import AuthService, UserService, TokenService, EmailActionTokenService, token_service

from app.infrastructure.repositories import UserRepository, EmailActionTokenRepository, BannedRefreshTokenRepository  
from app.infrastructure.config import get_settings

from . import SessionDep, MailServiceDep

settings = get_settings()


async def get_auth_service(
    session: SessionDep,
    mail_service: MailServiceDep,
):
    
    user_service = UserService(repository=UserRepository(session=session))
    email_action_service=EmailActionTokenService(repository=EmailActionTokenRepository(session=session))
    token_service=TokenService(user_service=user_service, repository=BannedRefreshTokenRepository(session=session))

    yield AuthService(
        user_service=user_service,
        email_action_service=email_action_service,
        token_service=token_service,
        mail_service=mail_service,
        transaction=SQLAlchemyTransaction(session=session)
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


