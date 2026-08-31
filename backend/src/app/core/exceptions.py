class NotFoundError(Exception): 
    """Resource not found."""

    pass


class DuplicateEntryError(Exception):
    """Duplicate entry."""

    def __init__(self, msg: str, duplicate_field: dict) -> None:
        self.msg = msg
        self.duplicate_field = duplicate_field

        super().__init__(msg)


class InvalidActionTokenError(Exception):
    """Mail token is invalid, expired, or already used."""

    pass

class InvalidVerificationError(Exception):
    """Verification token is invalid, expired, or already used."""

    pass


class InvalidCredentialsError(Exception):
    """Verification token is invalid, expired, or already used."""

    pass


class InvalidTokenError(Exception):
    """TokenPair is invalid, expired, or already used."""

    pass