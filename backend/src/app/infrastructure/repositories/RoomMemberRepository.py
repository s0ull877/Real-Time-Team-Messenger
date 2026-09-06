from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities import RoomMember
from app.core.interfaceRepositories import IRoomMemberRepository

from app.infrastructure.database.models import RoomMember as RoomMemberModel


class RoomMemberRepository(IRoomMemberRepository):

    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_entity(self, room_member_model: RoomMemberModel) -> RoomMember:

        return RoomMember(
            room_id=room_member_model.room_id,
            user_id=room_member_model.user_id,
            joined_at=room_member_model.joined_at
        )


    async def add(self, room_member: RoomMember) -> RoomMember:

        room_member_model = RoomMemberModel(
            room_id=room_member.room_id,
            user_id=room_member.user_id,
            joined_at=datetime.now(timezone.utc)
        )

        self.session.add(room_member_model)

        await self.session.flush()
        await self.session.refresh(room_member_model)

        return self._to_entity(room_member_model)
    

    async def remove(self, room_member: RoomMember) -> None:
        """
        Remove member from room.
        """
        return
    

    async def is_member(self, user_id: UUID, room_id: UUID) -> bool:
        """
        return whether the user is a member of the group
        """
        return
    

    async def get_room_members(self, room_id: UUID) -> list[RoomMember]:
        """
        Get room members
        """
        return
  