class NotFoundError(Exception): 
    """Resource not found."""

    pass


class DuplicateEntryError(Exception):
    """Duplicate entry."""

    def __init__(self, msg: str, duplicate_field: dict) -> None:
        self.msg = msg
        self.duplicate_field = duplicate_field

        super().__init__(msg)
