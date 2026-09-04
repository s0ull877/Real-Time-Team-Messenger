from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserRepositoryDTO:
    username: str
    email: str
    password_hash: str
    avatar_url: str | None = None
    is_verified: bool = False
