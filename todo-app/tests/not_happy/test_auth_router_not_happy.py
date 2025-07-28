import pytest
from fastapi.testclient import TestClient
from schemas.user import UserCreateRequest
from fastapi.security import OAuth2PasswordRequestForm
from utils.exceptions import UsernameExistsException, InvalidCredentialsException, UserNotFoundException, JWTDecodeException
from models.user import User
from jose import JWTError
from datetime import datetime
from utils.auth_utils import get_current_user
from utils.password_utils import get_password_hash

@pytest.mark.asyncio
async def test_register_user_username_exists(client, override_dependencies, mock_user_repo):
    hashed_password = get_password_hash("testpassword")
    mock_user_repo.get_user_by_username.return_value = User(id=1, username="testuser", email="test@example.com", password=hashed_password, created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    user_data = {"username": "testuser", "email": "new@example.com", "password": "testpassword"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}
    mock_user_repo.get_user_by_username.assert_called_once_with("testuser")

@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client, override_dependencies, mock_user_repo, mocker):
    hashed_password = get_password_hash("testpassword")
    mock_user_repo.get_user_by_username.return_value = User(id=1, username="testuser", email="test@example.com", password=hashed_password, created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    mocker.patch("utils.password_utils.verify_password", return_value=False)
    form_data = OAuth2PasswordRequestForm(username="testuser", password="wrongpassword", scope="")
    response = client.post("/auth/login", data={"username": form_data.username, "password": form_data.password})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    mock_user_repo.get_user_by_username.assert_called_once_with("testuser")

@pytest.mark.asyncio
async def test_login_user_not_found(client, override_dependencies, mock_user_repo):
    mock_user_repo.get_user_by_username.return_value = None
    form_data = OAuth2PasswordRequestForm(username="nonexistent", password="testpassword", scope="")
    response = client.post("/auth/login", data={"username": form_data.username, "password": form_data.password})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    mock_user_repo.get_user_by_username.assert_called_once_with("nonexistent")

@pytest.mark.asyncio
async def test_refresh_token_invalid(client, override_dependencies, mocker):
    mocker.patch("jose.jwt.decode", side_effect=JWTError)
    response = client.post("/auth/refresh?refresh_token=invalid_token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

@pytest.mark.asyncio
async def test_validate_token_invalid(client, mocker):
    mocker.patch("utils.auth_utils.get_current_user", side_effect=JWTDecodeException("Could not validate credentials"))
    response = client.post("/auth/validate-token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
