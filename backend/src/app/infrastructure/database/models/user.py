from sqlalchemy import VARCHAR, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import BaseModelMixin, Base



class User(Base, BaseModelMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        VARCHAR(50), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(255), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        VARCHAR(), nullable=False
    )
    avatar_url: Mapped[str | None] = mapped_column(
        VARCHAR(), nullable=True, default=None
    )
    is_verified: Mapped[bool] = mapped_column(
        BOOLEAN(), nullable=False, default=False
    )

    owned_rooms: Mapped[list["Room"]] = relationship(
        back_populates="owner",
    )

    room_members: Mapped[list["RoomMember"]] = relationship(
        back_populates="user",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="author",
    )

    email_action_tokens: Mapped[list["EmailActionToken"]] = relationship(
        back_populates="user",
    )