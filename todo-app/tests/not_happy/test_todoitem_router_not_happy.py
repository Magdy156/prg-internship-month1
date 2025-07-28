import pytest
from fastapi.testclient import TestClient
from schemas.todoitem import TodoItemCreate
from utils.exceptions import TodoItemNotFoundException, TodoListNotFoundException
from jose import JWTError
from unittest.mock import MagicMock
from dal.repositories.todoitem_repository import TodoItemRepository
from utils.dependencies import get_todoitem_repository
import logging

# Set up logging to debug mock application
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_todoitem_unauthorized(client, mock_auth_utils):
    _, _, decode_mock = mock_auth_utils
    decode_mock.side_effect = JWTError("Invalid token")
    todoitem_data = {
        "title": "Test TodoItem",
        "todolist_id": 1,
        "description": "Test description",
        "priority": "MEDIUM",
        "completed": False
    }
    response = client.post("/todoitems/", json=todoitem_data, headers={"Authorization": "Bearer invalid_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
    decode_mock.assert_called_once()

@pytest.mark.asyncio
async def test_read_todoitem_unauthorized(client, mock_auth_utils):
    _, _, decode_mock = mock_auth_utils
    decode_mock.side_effect = JWTError("Invalid token")
    response = client.get("/todoitems/1", headers={"Authorization": "Bearer invalid_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
    decode_mock.assert_called_once()

@pytest.mark.asyncio
async def test_read_todoitem_not_found(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    mock_todoitem_repo.get_todo_item.side_effect = TodoItemNotFoundException
    response = client.get("/todoitems/999", headers={"Authorization": "Bearer mocked_access_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoItem not found"}
    mock_todoitem_repo.get_todo_item.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_update_todoitem_not_found(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    mock_todoitem_repo.update_todo_item.side_effect = TodoItemNotFoundException
    todoitem_data = {
        "title": "Updated TodoItem",
        "todolist_id": 1,
        "description": "Updated description",
        "priority": "HIGH",
        "completed": True
    }
    response = client.put("/todoitems/999", json=todoitem_data, headers={"Authorization": "Bearer mocked_access_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoItem not found"}
    mock_todoitem_repo.update_todo_item.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todoitem_not_found(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    mock_todoitem_repo.delete_todo_item.side_effect = TodoItemNotFoundException
    response = client.delete("/todoitems/999", headers={"Authorization": "Bearer mocked_access_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoItem not found"}
    mock_todoitem_repo.delete_todo_item.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_create_todoitem_todolist_not_found(client, mock_db_session, override_dependencies, mock_current_user, fastapi_app_fixture):
    logger.debug("Setting up test_create_todoitem_todolist_not_found")
    # Create a real TodoItemRepository with mocked db session
    todoitem_repo = TodoItemRepository(mock_db_session)
    # Mock the database query to return None for the todolist
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = None
    mock_query.filter.return_value = mock_filter
    mock_db_session.query.return_value = mock_query
    logger.debug(f"Mocked mock_db_session.query: {mock_db_session.query}")
    # Override get_todoitem_repository to use the real repository
    fastapi_app_fixture.dependency_overrides[get_todoitem_repository] = lambda: todoitem_repo
    logger.debug(f"Set fastapi_app_fixture.dependency_overrides[get_todoitem_repository]: {fastapi_app_fixture.dependency_overrides.get(get_todoitem_repository)}")
    todoitem_data = {
        "title": "Test TodoItem",
        "todolist_id": 999,
        "description": "Test description",
        "priority": "MEDIUM",
        "completed": False
    }
    response = client.post("/todoitems/", json=todoitem_data, headers={"Authorization": "Bearer mocked_access_token"})
    logger.debug(f"Response status code: {response.status_code}, content: {response.json()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoList not found"}
    mock_db_session.query.assert_called_once()
