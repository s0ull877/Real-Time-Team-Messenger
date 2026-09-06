from typing import Annotated 
from fastapi import Depends

from app.core.services import AuthService

from app.infrastructure.config import get_settings

from . import UserServiceDep, EmailActionTokenServiceDep, TokenServiceDep, MailServiceDep

settings = get_settings()


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


