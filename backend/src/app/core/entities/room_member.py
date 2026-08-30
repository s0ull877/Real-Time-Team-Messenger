from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class RoomMember:
    room_id: UUID
    user_id: UUID
    joined_at: datetime | None = None