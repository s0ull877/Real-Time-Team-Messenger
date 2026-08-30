from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(slots=True)
class EmailMessage:
    email: str
    subject: str
    body: str

@dataclass(slots=True)
class EmailVerification:
    id: UUID | None = None
    user_id: UUID
    token_hash: str
    expires_at: datetime
    used_at: datetime | None = None
    created_at: datetime | None = None