import math
from uuid import UUID

from fastapi import APIRouter, Response, Request, HTTPException, status

from app.core.entities import TokenPair

from app.interface.dependencies import AuthServiceDep, CurrentUserIdDep, UserServiceDep
from app.interface.schemas import RegisterUser, UserResponse, LoginUser, PasswordBody, EmailBody
from app.infrastructure.config import get_settings, settings

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterUser,
    auth_service: AuthServiceDep
) -> UserResponse:
    """
    Create a new user.
    """
    
    user = await auth_service.register(email=user_data.email, username=user_data.username, password=user_data.password)

    return UserResponse.model_validate(user)


@router.get("/verify-email/{token}", status_code=status.HTTP_200_OK)
async def verify_email_by_token(
    token: UUID,
    auth_service: AuthServiceDep
) -> UserResponse:
    """
    """
    
    user = await auth_service.verify_email(token=str(token))

    return UserResponse.model_validate(user)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def send_new_verify_link(
    email_data: EmailBody,
    auth_service: AuthServiceDep,
) -> UserResponse:
    """
    """

    user = await auth_service.new_verify_email(email=email_data.email)

    return UserResponse.model_validate(user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    user_data: LoginUser,
    auth_service: AuthServiceDep
) -> None:
    """
    Login a user and return a JWT token.
    """
    token: TokenPair = await auth_service.login(user_data.email, user_data.password)

    response.set_cookie(
        key="access_token",
        value=token.access_token.token,
        httponly=True,
        secure=False if settings.debug else True,
        samesite="Lax",
        max_age=math.ceil(token.access_token.expires_at.total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token.token,
        httponly=True,
        secure=False if settings.debug else True,
        samesite="Lax",
        max_age=math.ceil(token.refresh_token.expires_at.total_seconds()),
    )
    return 


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthServiceDep
) -> None:
    """
    Logout a user
    """
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await auth_service.logout(refresh_token)
        response.delete_cookie(key="refresh_token")

    if access_token:
        response.delete_cookie(key="access_token")

    return 


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthServiceDep,
) -> None:
    """
    Refresh a user's JWT token.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No credentials provided",
        )
    
    token: TokenPair = await auth_service.refresh(refresh_token)

    response.set_cookie(
        key="access_token",
        value=token.access_token.token,
        httponly=True,
        secure=False if settings.debug else True,
        samesite="Lax",
        max_age=math.ceil(token.access_token.expires_at.total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token.token,
        httponly=True,
        secure=False if settings.debug else True,
        samesite="Lax",
        max_age=math.ceil(token.refresh_token.expires_at.total_seconds()),
    )

    return


@router.post("/request/reset-password", status_code=status.HTTP_200_OK)
async def request_reset_password(
    email_data: EmailBody,
    auth_service: AuthServiceDep
) -> None:

    await auth_service.request_password_reset(email=email_data.email)

    return


@router.post("/reset-password/{token}", status_code=status.HTTP_200_OK)
async def reset_password(
    token: UUID,
    password_data: PasswordBody,
    auth_service: AuthServiceDep
) -> UserResponse:

    user = await auth_service.reset_password(token=str(token), new_password=password_data.password)

    return UserResponse.model_validate(user)


@router.post("/request/change-email", status_code=status.HTTP_200_OK)
async def request_change_email(
    user_id: CurrentUserIdDep,
    email_data: EmailBody,
    auth_service: AuthServiceDep
) -> None:

    await auth_service.request_email_change(user_id=user_id, new_email=email_data.email)


@router.get("/change-email/{token}", status_code=status.HTTP_200_OK)
async def change_email(
    token: UUID,
    user_id: CurrentUserIdDep, 
    auth_service: AuthServiceDep
) -> UserResponse:

    user = await auth_service.change_email(user_id=user_id, token=str(token))

    return UserResponse.model_validate(user)