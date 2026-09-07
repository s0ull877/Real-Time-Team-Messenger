from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoomMemberResponse(BaseModel):

    room_id: UUID
    user_id: UUID
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateRoom(BaseModel):

    name: str


class UpdateRoom(CreateRoom):
    ...


class RoomResponse(BaseModel):

    id: UUID
    name: str
    owner_id: UUID

    model_config = ConfigDict(from_attributes=True)


class InviteRoom(BaseModel):

    username: str = Field(min_length=8, max_length=50)

