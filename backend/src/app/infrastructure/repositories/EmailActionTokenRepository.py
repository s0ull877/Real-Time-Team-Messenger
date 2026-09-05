from uuid import UUID
from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.entities import EmailActionToken, ActionEnum
from app.core.exceptions import NotFoundError
from app.core.interfaceRepositories import IEmailActionTokenRepository

from app.infrastructure.database.models import EmailActionToken as EmailActionTokenModel


class EmailActionTokenRepository(IEmailActionTokenRepository):
    """
    Interface for the user repository.
    """
    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, email_token_actionModel: EmailActionTokenModel) -> EmailActionToken:
        """
        Convert a UserModel instance to a User entity.
        """
        return EmailActionToken(
            email=email_token_actionModel.email,
            token_hash=email_token_actionModel.token_hash,
            action=email_token_actionModel.action,
            expires_at=email_token_actionModel.expires_at,
            used_at=email_token_actionModel.used_at
        )


    async def create(self, email_token_action: EmailActionToken) -> EmailActionToken:
        """
        Create a new email action token.

        @dataclass(slots=True)
        class EmailActionToken:
            user_id: UUID
            token_hash: str
            action: ActionEnum
            expires_at: datetime
            id: UUID | None = None
            used_at: datetime | None = None

        Raises:
            IntegrityError: If a database integrity constraint is violated.
        """
        email_token_actionModel = EmailActionTokenModel(
            email=email_token_action.email,
            token_hash=email_token_action.token_hash,
            action=email_token_action.action,
            expires_at=email_token_action.expires_at,
            used_at=None
        )

        self.session.add(email_token_actionModel)

        try:
            await self.session.commit()
            await self.session.refresh(email_token_actionModel)
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(email_token_actionModel)
    

    async def get_by_token_hash(self, token_hash: str) -> EmailActionToken | None:
        """
        Get a email action token by token_hash.

        Returns:
            EmailActionToken entity if the email action token exists, otherwise None.
        """
        stmt = select(EmailActionTokenModel) \
            .where(EmailActionTokenModel.token_hash == token_hash)

        result = await self.session.execute(stmt)

        email_token_actionModel = result.scalar_one_or_none()

        if email_token_actionModel is None:
            return None

        return self._to_entity(email_token_actionModel)

    
    async def mark_as_used(self, token_hash: str, used_at: datetime) -> EmailActionToken:
        """
        Update used_at field by EmailActionToken id.

        Raises:
            NotFoundError: If the user does not exist.
            IntegrityError: If a database integrity constraint is violated.
        """
        stmt = (
            update(EmailActionTokenModel)
            .where(EmailActionTokenModel.token_hash == token_hash)
            .values(used_at=used_at)
            .returning(EmailActionTokenModel)
        )

        result = await self.session.execute(stmt)
        email_token_actionModel = result.scalar_one_or_none()

        if email_token_actionModel is None:
            await self.session.rollback()
            raise NotFoundError(
                f"Email action token with token:{token_hash} not found"
            )

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(email_token_actionModel)
    

    async def delete_by_email_and_action(self, email: UUID, action: ActionEnum) -> None:
        """
        Delete all email action token by user_id and action.

        Raise NotFoundError if the user does not exist.
        """
        stmt = delete(EmailActionTokenModel)\
            .where(EmailActionTokenModel.email == email, EmailActionTokenModel.action == action)

        result = await self.session.execute(stmt)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
    