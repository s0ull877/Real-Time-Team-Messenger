from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

from app.core.entities import RoomMember, RoomServiceDTO
from app.interface.dependencies.token import get_current_user_id
from app.interface.dependencies.room import get_room_service


def test_create_room(client, app):
    user_id = uuid4()
    room_id = uuid4()
    joined_at = datetime.now(timezone.utc)

    owner = RoomMember(
        room_id=room_id,
        user_id=user_id,
        joined_at=joined_at,
    )

    room = RoomServiceDTO(
        id=room_id,
        name="Test Room",
        owner_id=user_id,
        room_members=[owner],
    )

    room_service = AsyncMock()
    room_service.create_room.return_value = room

    app.dependency_overrides[get_current_user_id] = lambda: user_id
    app.dependency_overrides[get_room_service] = lambda: room_service

    response = client.post(
        "/rttm/rooms",
        json={
            "name": "Test Room",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == str(room_id)
    assert data["name"] == "Test Room"
    assert data["owner_id"] == str(user_id)

    assert len(data["room_members"]) == 1
    assert data["room_members"][0]["room_id"] == str(room_id)
    assert data["room_members"][0]["user_id"] == str(user_id)
    assert data["room_members"][0]["joined_at"] is not None

    room_service.create_room.assert_awaited_once_with(
        owner_id=user_id,
        room_name="Test Room",
    )