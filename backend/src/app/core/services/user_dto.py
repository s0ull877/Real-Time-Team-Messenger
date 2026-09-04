from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    username: str
    email: str
    password: str
