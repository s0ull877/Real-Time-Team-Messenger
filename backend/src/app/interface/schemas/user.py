from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, \
    HttpUrl, field_validator, Field

from app.core.exceptions import InvalidURLSchema


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    email: EmailStr
    username: str
    avatar_url: str | None
    is_verified: bool


class UserProfileResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    username: str = Field(min_length=8, max_length=50)
    avatar_url: str | None


class UserProfileRequest(UserProfileResponse):

    @field_validator('avatar_url')
    def case_insensitive_image_extensions(cls, v: HttpUrl | None) -> HttpUrl | None:
        if v is not None:
            # Convert URL to string to check file extension
            url_str = str(v).lower()
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

            if not url_str.endswith(valid_extensions):
                raise InvalidURLSchema('Avatar must be a valid image URL (.jpg, .png, .webp, .gif)')

        return v

