from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoomMember(BaseModel):

    room_id: UUID
    user_id: UUID
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateRoom(BaseModel):

    name: str


class RoomResponse(BaseModel):

    id: UUID
    name: str
    owner_id: UUID
    members: list[RoomMember]

    model_config = ConfigDict(from_attributes=True)

