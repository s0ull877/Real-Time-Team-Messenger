from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

@dataclass(slots=True)
class RoomMember:
    room_id: UUID
    user_id: UUID
    joined_at: datetime | None = None


@dataclass(slots=True)
class Room:
    name: str
    owner_id: UUID
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
