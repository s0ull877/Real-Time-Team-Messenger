import uuid

from sqlalchemy import VARCHAR, ForeignKey, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModelMixin, Base


class Room(Base, BaseModelMixin):
    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(
        VARCHAR(100), nullable=False
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete=None),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="owned_rooms",
    )

    members: Mapped[list["RoomMember"]] = relationship(
        back_populates="room",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="room",
    )

    __table_args__ = (
        Index("ix_rooms_owner_id", "owner_id"),
    )
