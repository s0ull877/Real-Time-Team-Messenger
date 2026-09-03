from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    email: EmailStr
    username: str
    avatar_url: str | None
    is_verified: bool


class UserMember:

    id: UUID
    username: str
    avatar_url: str | None
