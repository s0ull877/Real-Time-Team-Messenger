from uuid import uuid4

from unittest.mock import AsyncMock

from app.core.entities.user import User
from app.interface.dependencies.user import get_user_service
from app.interface.dependencies.token import get_current_user_id



def test_get_user_info_returns_full_user_for_current_user(client, app):
    user_id = uuid4()

    user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        password_hash="hashed-password",
        avatar_url="https://example.com/avatar.png",
        is_verified=True,
    )

    user_service = AsyncMock()
    user_service.get_by_username.return_value = user

    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[get_current_user_id] = lambda: user_id

    response = client.get("/rttm/users/testuser")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user_id)
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["avatar_url"] == "https://example.com/avatar.png"
    assert data["is_verified"] is True

    user_service.get_by_username.assert_awaited_once_with(username="testuser")


def test_get_user_info_returns_profile_for_other_user(client, app):
    current_user_id = uuid4()
    another_user_id = uuid4()

    user = User(
        id=another_user_id,
        username="otheruser",
        email="other@example.com",
        password_hash="hashed-password",
        avatar_url="https://example.com/avatar.png",
        is_verified=True,
    )

    user_service = AsyncMock()
    user_service.get_by_username.return_value = user

    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[get_current_user_id] = lambda: current_user_id

    response = client.get("/rttm/users/otheruser")

    assert response.status_code == 200

    data = response.json()

    assert data["avatar_url"] == "https://example.com/avatar.png"
    assert data["username"] == "otheruser"

    # Для другого пользователя приватные данные не должны возвращаться.
    assert "email" not in data
    assert "password_hash" not in data
    assert "is_verified" not in data
    assert "id" not in data

    assert data["avatar_url"] == "https://example.com/avatar.png"

    user_service.get_by_username.assert_awaited_once_with(username="otheruser")


def test_update_my_profile(client, app):
    user_id = uuid4()

    updated_user = User(
        id=user_id,
        username="newusername",
        email="test@example.com",
        password_hash="hashed-password",
        avatar_url="https://example.com/avatar.png",
        is_verified=True,
    )

    user_service = AsyncMock()
    user_service.update_profile_data.return_value = updated_user

    app.dependency_overrides[get_user_service] = lambda: user_service
    app.dependency_overrides[get_current_user_id] = lambda: user_id

    response = client.post(
        "/rttm/users/me",
        json={
            "username": "newusername",
            "avatar_url": "https://example.com/avatar.png",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "newusername"
    assert data["avatar_url"] == "https://example.com/avatar.png"

    user_service.update_profile_data.assert_awaited_once_with(
        user_id=user_id,
        username="newusername",
        avatar_url="https://example.com/avatar.png",
    )