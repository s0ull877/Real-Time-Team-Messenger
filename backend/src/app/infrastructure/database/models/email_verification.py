import uuid
import enum
from datetime import datetime
from sqlalchemy import VARCHAR, ForeignKey, DateTime, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

class ActionEnum(enum.Enum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"
    CHANGE_EMAIL = "change_email"

class EmailActionToken(Base):
    __tablename__ = "email_actions_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token_hash: Mapped[str] = mapped_column(
        VARCHAR(64),
        nullable=False,
        unique=True,
    )
    action: Mapped[ActionEnum] = mapped_column(
        Enum(ActionEnum), nullable=False
    )
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),nullable=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    
    user: Mapped["User"] = relationship(
        back_populates="email_action_tokens",
    )