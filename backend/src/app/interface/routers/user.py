from fastapi import APIRouter, status

from app.interface.dependencies import CurrentUserIdDep, UserServiceDep
from app.interface.schemas import UserResponse, UserProfileRequest, UserProfileResponse


router = APIRouter(prefix="/users", tags=["user"])

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_user_info(
    username: str,
    user_id: CurrentUserIdDep,
    user_service: UserServiceDep
) -> UserResponse | UserProfileResponse:
    """
    Get user profile information by username
    If username == current user return full information
    """
    user = await user_service.get_by_username(username=username)

    if user.id == user_id:

        return UserResponse.model_validate(user)

    else:

        return UserProfileResponse.model_validate(user)


@router.post("/me", status_code=status.HTTP_200_OK)
async def update_my_profile(
    user_id: CurrentUserIdDep,
    user_data: UserProfileRequest,
    user_service: UserServiceDep
) -> UserResponse:
    """
    Get user profile information by username
    If username == current user return full information
    """
    user = await user_service.update_profile_data(
        user_id=user_id,
        username=user_data.username,
        avatar_url=user_data.avatar_url
    )

    return UserResponse.model_validate(user)