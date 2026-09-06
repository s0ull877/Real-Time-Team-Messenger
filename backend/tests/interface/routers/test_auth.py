from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

from app.core.entities import AccessToken, RefreshToken, TokenPair
from app.core.entities.user import User
from app.interface.dependencies.auth import get_auth_service
from app.interface.dependencies.token import get_current_user_id


def create_user() -> User:
    return User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        password_hash="hashed-password",
        avatar_url="https://example.com/avatar.png",
        is_verified=True,
    )


def create_token_pair() -> TokenPair:
    return TokenPair(
        access_token=AccessToken(
            token="access-token",
            expires_at=timedelta(minutes=15),
        ),
        refresh_token=RefreshToken(
            token="refresh-token",
            jti="refresh-jti",
            expires_at=timedelta(days=7),
        ),
    )


def test_register(client, app):
    user = create_user()

    auth_service = AsyncMock()
    auth_service.register.return_value = user

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.post(
        "/rttm/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser123",
            "password": "Password123"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["username"] == user.username
    assert data["avatar_url"] == user.avatar_url
    assert data["is_verified"] is True

    auth_service.register.assert_awaited_once_with(
        email="test@example.com",
        username="testuser123",
        password="Password123"
    )


def test_verify_email_by_token(client, app):
    user = create_user()
    token = uuid4()

    auth_service = AsyncMock()
    auth_service.verify_email.return_value = user

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.get(
        f"/rttm/auth/verify-email/{token}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["username"] == user.username

    auth_service.verify_email.assert_awaited_once_with(
        token=str(token),
    )


def test_send_new_verify_link(client, app):
    user = create_user()

    auth_service = AsyncMock()
    auth_service.new_verify_email.return_value = user

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.post(
        "/rttm/auth/verify-email",
        json={
            "email": "test@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["username"] == user.username

    auth_service.new_verify_email.assert_awaited_once_with(
        email="test@example.com",
    )


def test_login(client, app):
    token_pair = create_token_pair()

    auth_service = AsyncMock()
    auth_service.login.return_value = token_pair

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.post(
        "/rttm/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    assert response.cookies.get("access_token") == "access-token"
    assert response.cookies.get("refresh_token") == "refresh-token"

    auth_service.login.assert_awaited_once_with(
        "test@example.com",
        "Password123",
    )


def test_logout_with_tokens(client, app):
    auth_service = AsyncMock()

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    client.cookies.set("access_token", "access-token")
    client.cookies.set("refresh_token", "refresh-token")

    response = client.get(
        "/rttm/auth/logout",
    )

    assert response.status_code == 200

    auth_service.logout.assert_awaited_once_with(
        "refresh-token",
    )

    set_cookie_headers = response.headers.get_list("set-cookie")
    
    assert any(
        "refresh_token=" in header and "Max-Age=0" in header
        for header in set_cookie_headers
    )

    assert any(
        "access_token=" in header and "Max-Age=0" in header
        for header in set_cookie_headers
    )


def test_logout_without_refresh_token(client, app):
    auth_service = AsyncMock()

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.get(
        "/rttm/auth/logout",
    )

    assert response.status_code == 200

    auth_service.logout.assert_not_awaited()


def test_refresh_without_token(client, app):
    auth_service = AsyncMock()

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.get(
        "/rttm/auth/refresh",
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "No credentials provided"

    auth_service.refresh.assert_not_awaited()


def test_refresh(client, app):
    token_pair = create_token_pair()

    auth_service = AsyncMock()
    auth_service.refresh.return_value = token_pair

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    client.cookies.set(
        "refresh_token",
        "old-refresh-token",
    )

    response = client.get(
        "/rttm/auth/refresh",
    )

    assert response.status_code == 200

    assert response.cookies.get("access_token") == "access-token"
    assert response.cookies.get("refresh_token") == "refresh-token"

    auth_service.refresh.assert_awaited_once_with(
        "old-refresh-token",
    )


def test_request_reset_password(client, app):
    auth_service = AsyncMock()

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.post(
        "/rttm/auth/request/reset-password",
        json={
            "email": "test@example.com",
        },
    )

    assert response.status_code == 200

    auth_service.request_password_reset.assert_awaited_once_with(
        email="test@example.com",
    )


def test_reset_password(client, app):
    user = create_user()
    token = uuid4()

    auth_service = AsyncMock()
    auth_service.reset_password.return_value = user

    app.dependency_overrides[get_auth_service] = lambda: auth_service

    response = client.post(
        f"/rttm/auth/reset-password/{token}",
        json={
            "password": "NewPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["username"] == user.username

    auth_service.reset_password.assert_awaited_once_with(
        token=str(token),
        new_password="NewPassword123",
    )


def test_request_change_email(client, app):
    user_id = uuid4()

    auth_service = AsyncMock()

    app.dependency_overrides[get_auth_service] = lambda: auth_service
    app.dependency_overrides[get_current_user_id] = lambda: user_id

    response = client.post(
        "/rttm/auth/request/change-email",
        json={
            "email": "new@example.com",
        },
    )

    assert response.status_code == 200

    auth_service.request_email_change.assert_awaited_once_with(
        user_id=user_id,
        new_email="new@example.com",
    )


def test_change_email(client, app):
    user_id = uuid4()
    token = uuid4()
    user = create_user()

    auth_service = AsyncMock()
    auth_service.change_email.return_value = user

    app.dependency_overrides[get_auth_service] = lambda: auth_service
    app.dependency_overrides[get_current_user_id] = lambda: user_id

    response = client.get(
        f"/rttm/auth/change-email/{token}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["username"] == user.username

    auth_service.change_email.assert_awaited_once_with(
        user_id=user_id,
        token=str(token),
    )