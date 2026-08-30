import jwt
from uuid import UUID, uuid4
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from app.infrastructure.config import get_settings
from app.core.exceptions import NotFoundError, InvalidTokenError
from app.core.entities import RefreshToken, AccessToken, TokenPair, User
from app.core.interfaceRepositories import IBannedRefreshTokenRepository

from . import UserService


settings = get_settings()


@dataclass
class TokenService:

    user_service: UserService
    repository: IBannedRefreshTokenRepository


    def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )
        except jwt.PyJWTError as exc:
            raise InvalidTokenError("Invalid token") from exc


    def _get_user_id_from_payload(self, payload: dict) -> UUID:
        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenError("Invalid token")

        try:
            return UUID(user_id)
        except ValueError as exc:
            raise InvalidTokenError("Invalid token") from exc

     
    def create_refresh_token(self, data: dict) -> RefreshToken:

        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )

        return RefreshToken(
            token=encoded_jwt,
            type="Bearer",
            expires=timedelta(days=settings.refresh_token_expire_days),
            jti=data["jti"],
        )


    def create_access_token(self, data: dict) -> AccessToken:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire, "type": "access"})

        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )

        return AccessToken(
            token=encoded_jwt,
            type="Bearer",
            expires=timedelta(minutes=settings.access_token_expire_minutes),
        )

    async def refresh(self, token: str) -> TokenPair:
        """
        Refresh a user's JWT token.
        """
        payload = self._decode_token(token=token)

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")
        
        user_id = self._get_user_id_from_payload(payload)
        user = await self.user_service.get_by_id(user_id=user_id)
        
        jti = payload.get("jti")
        if jti is None:
            raise InvalidTokenError("Invalid token")
        
        banned_token = (
            await self.repository.is_banned(jti=jti)
        )
        
        if banned_token:
            raise InvalidTokenError("Refresh token is banned")
        
        await self.repository.ban(jti=jti)
        
        access_token = self.create_access_token(
            {"sub": str(user.id)}
        )
        refresh_token = self.create_refresh_token(
            {"sub": str(user.id), "jti": str(uuid4())}
        )
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    
    async def verify_access_token(self, token: str) -> bool:

        try:

            payload = self._decode_token(token=token)

            if payload.get("type") != "access":
                return None
            
            user_id = self._get_user_id_from_payload(payload)
            return await self.user_service.get_by_id(user_id=user_id)
        
        except (NotFoundError, InvalidTokenError):
            return None


    async def verify_refresh_token(self, token: str) -> User | None:

        try:

            payload = self._decode_token(token=token)

            if payload.get("type") != "refresh":
                return None
            
            user_id = self._get_user_id_from_payload(payload)
            user = await self.user_service.get_by_id(user_id=user_id)
            
            jti = payload.get("jti")
            if jti is None:
                return None
            
            banned_token = (
                await self.repository.is_banned(
                    jti=jti
                )
            )
            if banned_token:
                return None
            
            return user
        
        except (NotFoundError, InvalidTokenError):
            return None