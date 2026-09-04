from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base, utc_now


class BannedRefreshToken(Base):
    __tablename__ = "banned_refresh_tokens"

    jti: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        nullable=False,
    )

    banned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )