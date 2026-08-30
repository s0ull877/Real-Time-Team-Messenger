import hashlib
from uuid import UUID, uuid4
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.core.entities import EmailVerification
from app.core.interfaceRepositories import IEmailVerificationRepository
from app.core.exceptions import InvalidVerificationError



@dataclass
class EmailVerificationService:
    
    repository: IEmailVerificationRepository

    async def create(self, user_id: UUID) -> tuple[EmailVerification, str]:
        """
        Create EmailVerification. 
        Return tuple (created EmailVerification entity, raw token string for sending)
        """
        await self.repository.delete_by_user_id(user_id=user_id)

        token = str(uuid4())
        email_verification = EmailVerification(
            user_id=user_id,
            token_hash=hashlib.sha256(token.encode()).hexdigest(),
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )

        created = await self.repository.create(email_verification)
        return (created, token)


    async def verify(self, user_id: UUID, token: str) -> EmailVerification:
        """
        Verify email verification token.

        If token does not exist, belongs to another user, has already been used,
        or has expired, raise InvalidVerificationError.

        If verification is valid, mark it as used and return it.
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        email_verification = await self.repository.get_by_token_hash(token_hash=token_hash)

        if not email_verification:
            raise InvalidVerificationError("Verification token is invalid.")

        if email_verification.user_id != user_id:
            raise InvalidVerificationError("Verification token is invalid.")

        if email_verification.used_at:
            raise InvalidVerificationError("Verification token has already been used.")

        if email_verification.expires_at <= datetime.now(timezone.utc):
            raise InvalidVerificationError("Verification token has expired.")

        return await self.repository.mark_as_used(email_verification_id=email_verification.id, used_at=datetime.now(timezone.utc))





  