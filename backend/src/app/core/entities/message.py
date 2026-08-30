from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Message:
    id: UUID | None = None
    room_id: UUID
    author_id: UUID
    encrypted_text: str
    deleted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None