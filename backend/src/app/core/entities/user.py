from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    id: UUID | None = None
    username: str
    email: str
    password_hash: str
    avatar_url: str | None
    is_verified: bool
    created_at: datetime
    updated_at: datetime