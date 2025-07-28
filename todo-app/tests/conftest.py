import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.orm import Session
from main import app as fastapi_app  # Rename import to avoid conflict
from models.user import User
from schemas.todolist import TodoListResponse
from schemas.todoitem import TodoItemResponse
from schemas.user import UserCreateResponse, UserReadResponse, UserUpdateResponse
from schemas.token import TokenResponse
from utils.auth_utils import get_current_user, create_access_token, create_refresh_token
from dal.repositories.todolist_repository import TodoListRepository
from dal.repositories.todoitem_repository import TodoItemRepository
from dal.repositories.user_repository import UserRepository
from utils.dependencies import get_todolist_repository, get_todoitem_repository, get_user_service
from utils.auth_dependencies import AuthService, get_auth_service
from services.user_service import UserService
from datetime import datetime

@pytest.fixture
def fastapi_app_fixture():
    return fastapi_app  # Return the FastAPI app instance

@pytest.fixture
def client():
    return TestClient(fastapi_app)

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_todolist_repo(mock_db_session):
    repo = MagicMock(spec=TodoListRepository)
    repo.create_todo.return_value = TodoListResponse(id=1, title="Test Todo", user_id=1, created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.get_todo.return_value = TodoListResponse(id=1, title="Test Todo", user_id=1, created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.update_todo.return_value = TodoListResponse(id=1, title="Updated Todo", user_id=1, created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.delete_todo.return_value = None
    return repo

@pytest.fixture
def mock_todoitem_repo(mock_db_session):
    repo = MagicMock(spec=TodoItemRepository)
    repo.create_todo_item.return_value = TodoItemResponse(id=1, title="Test Item", todolist_id=1, completed=False, priority="MEDIUM", created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.get_todo_item.return_value = TodoItemResponse(id=1, title="Test Item", todolist_id=1, completed=False, priority="MEDIUM", created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.update_todo_item.return_value = TodoItemResponse(id=1, title="Updated Item", todolist_id=1, completed=True, priority="HIGH", created_at="2025-07-28T18:25:00Z", updated_at="2025-07-28T18:25:00Z")
    repo.delete_todo_item.return_value = None
    return repo

@pytest.fixture
def mock_user_repo(mock_db_session):
    repo = MagicMock(spec=UserRepository)
    repo.create_user.return_value = UserReadResponse(id=1, username="testuser", email="test@example.com", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    repo.get_user_by_id.return_value = User(id=1, username="testuser", email="test@example.com", password="$2b$12$z8y9x0w1v2u3t4r5s6q7r8.t9u0v1w2x3y4z5A6B7C8D9E0F1G2H3", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    repo.get_user_by_username.return_value = User(id=1, username="testuser", email="test@example.com", password="$2b$12$z8y9x0w1v2u3t4r5s6q7r8.t9u0v1w2x3y4z5A6B7C8D9E0F1G2H3", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    repo.update_user.return_value = UserUpdateResponse(id=1, username="updateduser", email="updated@example.com", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))
    repo.delete_user.return_value = None
    return repo

@pytest.fixture
def mock_current_user():
    return User(id=1, username="testuser", email="test@example.com", password="$2b$12$z8y9x0w1v2u3t4r5s6q7r8.t9u0v1w2x3y4z5A6B7C8D9E0F1G2H3", created_at=datetime.fromisoformat("2025-07-28T18:25:00"))

@pytest.fixture(scope="function")
def mock_auth_utils(mocker, request):
    print("Applying mock_auth_utils")
    access_mock = mocker.patch("services.auth_service.create_access_token", return_value="mocked_access_token")
    refresh_mock = mocker.patch("services.auth_service.create_refresh_token", return_value="mocked_refresh_token")
    mocker.patch("utils.password_utils.verify_password", return_value=True)
    decode_mock = mocker.patch("jose.jwt.decode", return_value={"sub": "testuser"})
    yield access_mock, refresh_mock, decode_mock

@pytest.fixture
def override_dependencies(mock_todolist_repo, mock_todoitem_repo, mock_user_repo, mock_current_user, mock_auth_utils):
    fastapi_app.dependency_overrides[get_todolist_repository] = lambda: mock_todolist_repo
    fastapi_app.dependency_overrides[get_todoitem_repository] = lambda: mock_todoitem_repo
    fastapi_app.dependency_overrides[get_user_service] = lambda: UserService(mock_user_repo)
    fastapi_app.dependency_overrides[get_auth_service] = lambda: AuthService(UserService(mock_user_repo))
    fastapi_app.dependency_overrides[get_current_user] = lambda: mock_current_user
    yield
    fastapi_app.dependency_overrides.clear()
