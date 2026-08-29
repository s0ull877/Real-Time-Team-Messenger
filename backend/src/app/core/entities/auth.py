from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class AccessToken:
    token: str
    expires_at: datetime
    token_type: str = "Bearer"


@dataclass(slots=True)
class RefreshToken:
    token: str
    jti: str
    expires_at: datetime
    token_type: str = "Bearer"


@dataclass(slots=True)
class TokenPair:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass(slots=True)
class BannedRefreshToken:
    jti: str
    banned_at: datetime


@dataclass(slots=True)
class EmailVerification:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    used_at: datetime | None
    created_at: datetime