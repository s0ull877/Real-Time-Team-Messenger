import jwt
from uuid import UUID
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.infrastructure.config import get_settings
from app.core.services import TokenService
from app.infrastructure.repositories import BannedRefreshTokenRepository

from . import UserServiceDep, SessionDep

settings = get_settings()


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

JWTBearerDep = Annotated[
    dict,
    Depends(JWTBearer()),
]

async def get_current_user_id(
    payload: JWTBearerDep,
) -> UUID:
    return UUID(payload["sub"])

CurrentUserIdDep = Annotated[
    UUID,
    Depends(get_current_user_id),
]