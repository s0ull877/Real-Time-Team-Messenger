from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    email: EmailStr
    username: str
    avatar_url: str | None
    is_verified: bool


class UserConflictResponse(BaseModel):
    detail: str
    field: str


class UserMember(BaseModel):

    id: UUID
    username: str
    avatar_url: str | None
