from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Room:
    id: UUID | None = None
    name: str
    owner_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None