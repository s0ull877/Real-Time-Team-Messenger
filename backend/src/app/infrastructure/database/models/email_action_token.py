import uuid
import enum
from datetime import datetime
from sqlalchemy import VARCHAR, ForeignKey, DateTime, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

from app.core.entities import ActionEnum

class EmailActionToken(Base):
    __tablename__ = "email_actions_tokens"

    token_hash: Mapped[str] = mapped_column(
        VARCHAR(64),
        nullable=False,
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(
        VARCHAR(64),
        nullable=False,
        primary_key=True,
    )
    action: Mapped[ActionEnum] = mapped_column(
        Enum(
            ActionEnum,
            values_callable=lambda enum_class: [item.value for item in enum_class],
        ),
        nullable=False,
    )
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),nullable=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )