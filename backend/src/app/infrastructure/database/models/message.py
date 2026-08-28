import uuid
from datetime import datetime
from sqlalchemy import Text, ForeignKey, DateTime, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModelMixin, Base


class Message(Base, BaseModelMixin):
    __tablename__ = "messages"

    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )   
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete=None),
        nullable=False,
    )
    encrypted_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )


    author: Mapped["User"] = relationship(
        back_populates="messages",
    )

    room: Mapped[list["Room"]] = relationship(
        back_populates="messages",
    )


    __table_args__ = (
        Index(
            "ix_messages_room_created_at",
            "room_id",
            "created_at",
        ),
    )