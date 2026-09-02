from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    username: str
    email: str
    password_hash: str
    id: UUID | None = None
    avatar_url: str | None = None
    is_verified: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None