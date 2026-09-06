from typing import Annotated

from fastapi import Depends

from app.core.services import UserService
from app.infrastructure.repositories import UserRepository

from . import SessionDep, SQLAlchemyTransaction

async def get_user_service(
    session: SessionDep,
):
    repository = UserRepository(session=session)

    yield UserService(
        repository=repository,
        transaction=SQLAlchemyTransaction(session=session)
    )


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)
]