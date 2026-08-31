import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

class ActionEnum(enum.Enum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"
    CHANGE_EMAIL = "change_email"


@dataclass(slots=True)
class EmailMessage:
    email: str
    subject: str
    body: str

@dataclass(slots=True)
class EmailActionToken:
    user_id: UUID
    token_hash: str
    action: ActionEnum
    expires_at: datetime
    id: UUID | None = None
    used_at: datetime | None = None