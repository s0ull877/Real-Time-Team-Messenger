from sqlalchemy import select
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.entities import BannedRefreshToken
from app.core.interfaceRepositories import IBannedRefreshTokenRepository
from app.infrastructure.database.models import (
    BannedRefreshToken as BannedRefreshTokenModel,
)


class BannedRefreshTokenRepository(IBannedRefreshTokenRepository):

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(
        self,
        banned_token_model: BannedRefreshTokenModel,
    ) -> BannedRefreshToken:
        """
        Convert a BannedRefreshTokenModel instance to a BannedRefreshToken entity.
        """
        return BannedRefreshToken(
            jti=banned_token_model.jti,
            banned_at=banned_token_model.banned_at
        )


    async def ban(self, jti: str) -> BannedRefreshToken:
        """
        Ban a refresh token by its JTI.

        Raises:
            IntegrityError: If a database integrity constraint is violated.
        """
        banned_token_model = BannedRefreshTokenModel(
            jti=jti,
            banned_at=datetime.now(timezone.utc)
        )

        self.session.add(banned_token_model)

        try:
            await self.session.commit()
            await self.session.refresh(banned_token_model)
        except IntegrityError:
            await self.session.rollback()
            raise

        return self._to_entity(banned_token_model)


    async def is_banned(self, jti: str) -> bool:
        """
        Check whether a refresh token with the given JTI is banned.

        Returns:
            True if the token is banned, otherwise False.
        """
        stmt = select(BannedRefreshTokenModel).where(
            BannedRefreshTokenModel.jti == jti
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None