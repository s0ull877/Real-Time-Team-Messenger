from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class Room:
    name: str
    owner_id: UUID
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None