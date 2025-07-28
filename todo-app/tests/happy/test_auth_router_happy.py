import pytest
from fastapi.testclient import TestClient
from schemas.user import UserCreateRequest, UserCreateResponse, UserReadResponse
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from datetime import datetime
from utils.exceptions import UserNotFoundException
from utils.password_utils import get_password_hash

@pytest.mark.asyncio
async def test_register_user_success(client, override_dependencies, mock_user_repo):
    mock_user_repo.get_user_by_username.side_effect = UserNotFoundException  # Simulate no existing user
    mock_user_repo.create_user.return_value = UserCreateResponse(id=1, username="testuser", email="test@example.com", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "testuser", "email": "test@example.com", "created_at": "2025-07-28T18:25:00"}
    mock_user_repo.get_user_by_username.assert_called_once_with("testuser")
    mock_user_repo.create_user.assert_called_once()

@pytest.mark.asyncio
async def test_login_user_success(client, override_dependencies, mock_user_repo, mock_auth_utils):
    access_mock, refresh_mock, decode_mock = mock_auth_utils  # Unpack all three mocks
    hashed_password = get_password_hash("testpassword")
    mock_user_repo.get_user_by_username.return_value = User(id=1, username="testuser", email="test@example.com", password=hashed_password, created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    form_data = OAuth2PasswordRequestForm(username="testuser", password="testpassword", scope="")
    response = client.post("/auth/login", data={"username": form_data.username, "password": form_data.password})
    assert response.status_code == 200
    assert response.json() == {"access_token": "mocked_access_token", "refresh_token": "mocked_refresh_token", "token_type": "bearer"}
    mock_user_repo.get_user_by_username.assert_called_once_with("testuser")
    access_mock.assert_called_once()
    refresh_mock.assert_called_once()

@pytest.mark.asyncio
async def test_refresh_token_success(client, override_dependencies, mock_user_repo, mock_auth_utils):
    access_mock, refresh_mock, decode_mock = mock_auth_utils  # Unpack all three mocks
    hashed_password = get_password_hash("testpassword")
    mock_user_repo.get_user_by_username.return_value = User(id=1, username="testuser", email="test@example.com", password=hashed_password, created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    response = client.post("/auth/refresh?refresh_token=mocked_refresh_token")
    assert response.status_code == 200
    assert response.json() == {"access_token": "mocked_access_token", "refresh_token": None, "token_type": "bearer"}
    mock_user_repo.get_user_by_username.assert_called_once_with("testuser")
    access_mock.assert_called_once()

@pytest.mark.asyncio
async def test_validate_token_success(client, override_dependencies):
    response = client.post("/auth/validate-token")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "testuser", "email": "test@example.com", "created_at": "2025-07-28T18:25:00"}
