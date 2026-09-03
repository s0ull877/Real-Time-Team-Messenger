class AppError(Exception):
    """Base application error."""

    pass


class RepositoryError(AppError):
    """Base repository error."""

    pass


class ServiceError(AppError):
    """Base service error."""

    pass


class NotFoundError(AppError):
    """Resource not found."""

    pass


class DuplicateEntryError(ServiceError):
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
