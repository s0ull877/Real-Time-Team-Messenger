class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int,
        details: dict | None = None
    ):
        self.message = message
        self.details = details
        self.status_code = status_code

        super().__init__(message)


class NotFoundError(AppError): 
    """Resource not found."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=404,
        )


class DuplicateEntryError(AppError):
    """Duplicate entry."""

    def __init__(self, message: str, duplicate_field: dict) -> None:
        self.message = message
        self.details = {'duplicate_field': duplicate_field}

        super().__init__(
            message=message,
            status_code=409,
            details=self.details
        )


class InvalidActionTokenError(AppError):
    """Mail token is invalid, expired, or already used."""

    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(
            message=message,
            status_code=409
        )

class InvalidVerificationError(AppError):
    """Verification token is invalid, expired, or already used."""

    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(
            message=message,
            status_code=403
        )


class InvalidCredentialsError(Exception):
    """Verification token is invalid, expired, or already used."""

    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(
            message=message,
            status_code=401
        )


class InvalidTokenError(Exception):
    """TokenPair is invalid, expired, or already used."""

    def __init__(self, message: str) -> None:
        self.message = message

        super().__init__(
            message=message,
            status_code=401
        )