from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

from app.core.entities import RoomMember, Room
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

    room = Room(
        id=room_id,
        name="Test Room",
        owner_id=user_id,
        members=[owner],
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

    assert len(data["members"]) == 1
    assert data["members"][0]["room_id"] == str(room_id)
    assert data["members"][0]["user_id"] == str(user_id)
    assert data["members"][0]["joined_at"] is not None

    room_service.create_room.assert_awaited_once_with(
        owner_id=user_id,
        room_name="Test Room",
    )


def test_get_rooms(client, app):
    user_id = uuid4()

    room_1_id = uuid4()
    room_2_id = uuid4()

    joined_at_1 = datetime.now(timezone.utc)
    joined_at_2 = datetime.now(timezone.utc)

    room_1_member = RoomMember(
        room_id=room_1_id,
        user_id=user_id,
        joined_at=joined_at_1,
    )

    room_2_member = RoomMember(
        room_id=room_2_id,
        user_id=user_id,
        joined_at=joined_at_2,
    )

    rooms = [
        Room(
            id=room_1_id,
            name="Room 1",
            owner_id=user_id,
            members=[room_1_member],
        ),
        Room(
            id=room_2_id,
            name="Room 2",
            owner_id=user_id,
            members=[room_2_member],
        ),
    ]

    room_service = AsyncMock()
    room_service.get_rooms_by_member_id.return_value = rooms

    app.dependency_overrides[get_current_user_id] = lambda: user_id
    app.dependency_overrides[get_room_service] = lambda: room_service

    response = client.get("/rttm/rooms")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["id"] == str(room_1_id)
    assert data[0]["name"] == "Room 1"
    assert data[0]["owner_id"] == str(user_id)

    assert len(data[0]["members"]) == 1
    assert data[0]["members"][0]["room_id"] == str(room_1_id)
    assert data[0]["members"][0]["user_id"] == str(user_id)
    assert data[0]["members"][0]["joined_at"] is not None

    assert data[1]["id"] == str(room_2_id)
    assert data[1]["name"] == "Room 2"
    assert data[1]["owner_id"] == str(user_id)

    assert len(data[1]["members"]) == 1
    assert data[1]["members"][0]["room_id"] == str(room_2_id)
    assert data[1]["members"][0]["user_id"] == str(user_id)
    assert data[1]["members"][0]["joined_at"] is not None

    room_service.get_rooms_by_member_id.assert_awaited_once_with(
        member_id=user_id
    )



def test_get_owned_rooms(client, app):
    user_id = uuid4()

    room_1_id = uuid4()
    room_2_id = uuid4()

    joined_at_1 = datetime.now(timezone.utc)
    joined_at_2 = datetime.now(timezone.utc)

    room_1_member = RoomMember(
        room_id=room_1_id,
        user_id=user_id,
        joined_at=joined_at_1,
    )

    room_2_member = RoomMember(
        room_id=room_2_id,
        user_id=user_id,
        joined_at=joined_at_2,
    )

    rooms = [
        Room(
            id=room_1_id,
            name="Room 1",
            owner_id=user_id,
            members=[room_1_member],
        ),
        Room(
            id=room_2_id,
            name="Room 2",
            owner_id=user_id,
            members=[room_2_member],
        ),
    ]

    room_service = AsyncMock()
    room_service.get_owned_rooms.return_value = rooms

    app.dependency_overrides[get_current_user_id] = lambda: user_id
    app.dependency_overrides[get_room_service] = lambda: room_service

    response = client.get("/rttm/rooms/owned")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["id"] == str(room_1_id)
    assert data[0]["name"] == "Room 1"
    assert data[0]["owner_id"] == str(user_id)

    assert len(data[0]["members"]) == 1
    assert data[0]["members"][0]["room_id"] == str(room_1_id)
    assert data[0]["members"][0]["user_id"] == str(user_id)
    assert data[0]["members"][0]["joined_at"] is not None

    assert data[1]["id"] == str(room_2_id)
    assert data[1]["name"] == "Room 2"
    assert data[1]["owner_id"] == str(user_id)

    assert len(data[1]["members"]) == 1
    assert data[1]["members"][0]["room_id"] == str(room_2_id)
    assert data[1]["members"][0]["user_id"] == str(user_id)
    assert data[1]["members"][0]["joined_at"] is not None

    room_service.get_owned_rooms.assert_awaited_once_with(
        owner_id=user_id,
    )