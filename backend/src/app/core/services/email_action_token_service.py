import hashlib
from uuid import UUID, uuid4
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.core.entities import EmailActionToken, ActionEnum
from app.core.interfaceRepositories import IEmailActionTokenRepository
from app.core.exceptions import InvalidActionTokenError



@dataclass
class EmailActionTokenService:
    
    repository: IEmailActionTokenRepository

    async def create(self, user_id: UUID, action: ActionEnum, expires_in: timedelta = timedelta(hours=1)) -> tuple[EmailActionToken, str]:
        """
        Create EmailActionToken. 
        Return tuple (created EmailActionToken entity, raw token string for sending)
        """
        await self.repository.delete_by_user_id_and_action(user_id=user_id, action=action)

        token = str(uuid4())
        email_action_token = EmailActionToken(
            user_id=user_id,
            token_hash=hashlib.sha256(token.encode()).hexdigest(),
            action=action,
            expires_at=datetime.now(timezone.utc) + expires_in
        )

        created = await self.repository.create(email_action_token)
        return (created, token)


    async def verify(self, token: str) -> EmailActionToken:
        """
        Verify email verification token.

        If token does not exist, belongs to another user, has already been used,
        or has expired, raise InvalidVerificationError.

        If verification is valid, mark it as used and return it.
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        email_action_token = await self.repository.get_by_token_hash(token_hash=token_hash)

        if not email_action_token:
            raise InvalidActionTokenError("Verification token is invalid.")

        if email_action_token.used_at:
            raise InvalidActionTokenError("Verification token has already been used.")

        if email_action_token.expires_at <= datetime.now(timezone.utc):
            raise InvalidActionTokenError("Verification token has expired.")

        return await self.repository.mark_as_used(email_action_token_id=email_action_token.id, used_at=datetime.now(timezone.utc))





  