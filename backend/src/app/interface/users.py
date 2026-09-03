from fastapi import APIRouter, status

from app.core.services.user_dto import CreateUserDTO
from app.interface.dependencies import UserServiceDep
from app.interface.schemas import UserConflictResponse, UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": UserConflictResponse,
            "description": "Email or username already exists",
        },
    },
)
async def create_user(
    user_data: UserCreate,
    user_service: UserServiceDep,
) -> UserResponse:
    user = await user_service.create(
        CreateUserDTO(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
    )

    return UserResponse.model_validate(user)
