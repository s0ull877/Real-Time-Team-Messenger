from fastapi import APIRouter, status
from app.interface.dependencies import AuthServiceDep
from app.interface.schemas import RegisterUser, UserResponse

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