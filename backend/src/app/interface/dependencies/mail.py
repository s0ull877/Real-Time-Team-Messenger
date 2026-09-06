from typing import Annotated

from fastapi import Depends, Request

from app.core.services import EmailActionTokenService, MailService
from app.infrastructure.repositories import EmailActionTokenRepository

from .session import SessionDep



def get_mail_service(request: Request) -> MailService:
    kafka_producer = request.app.state.producer

    return MailService(
        broker_producer=kafka_producer,
    )


MailServiceDep = Annotated[
    MailService,
    Depends(get_mail_service),
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