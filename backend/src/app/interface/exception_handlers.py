from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.services.user_service import UserAlreadyExistsError


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "field": exc.field,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserAlreadyExistsError,
        user_already_exists_handler,
    )
