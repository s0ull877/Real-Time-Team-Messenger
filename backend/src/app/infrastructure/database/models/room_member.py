import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base, utc_now


class RoomMember(Base):
    __tablename__ = "room_members"

    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        primary_key=True, nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True, nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    user: Mapped["User"] = relationship(
        back_populates="room_members",
    )

    room: Mapped["Room"] = relationship(
        back_populates="members",
    )


    __table_args__ = (
        Index("ix_room_members_user_id", "user_id"),
    )