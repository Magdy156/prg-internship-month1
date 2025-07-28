import pytest
from fastapi.testclient import TestClient
from schemas.todolist import TodoListCreate, TodoListResponse
from models.todolist import TodoList
from models.user import User
from datetime import datetime, timezone
from utils.password_utils import get_password_hash

@pytest.mark.asyncio
async def test_create_todolist_success(client, override_dependencies, mock_todolist_repo, mock_current_user):
    todolist_data = {"title": "Test TodoList"}
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    mock_todolist_repo.create_todo.return_value = TodoListResponse(
        id=1, title="Test TodoList", user_id=mock_current_user.id, created_at=created_at, updated_at=created_at
    )
    response = client.post("/todolists/", json=todolist_data, headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test TodoList",
        "user_id": mock_current_user.id,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:25:00"
    }
    mock_todolist_repo.create_todo.assert_called_once()

@pytest.mark.asyncio
async def test_read_todolist_success(client, override_dependencies, mock_todolist_repo, mock_current_user):
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    mock_todolist_repo.get_todo.return_value = TodoListResponse(
        id=1, title="Test TodoList", user_id=mock_current_user.id, created_at=created_at, updated_at=created_at
    )
    response = client.get("/todolists/1", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test TodoList",
        "user_id": mock_current_user.id,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:25:00"
    }
    mock_todolist_repo.get_todo.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_todolist_success(client, override_dependencies, mock_todolist_repo, mock_current_user):
    todolist_data = {"title": "Updated TodoList"}
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    updated_at = datetime.fromisoformat("2025-07-28T18:30:00")
    mock_todolist_repo.update_todo.return_value = TodoListResponse(
        id=1, title="Updated TodoList", user_id=mock_current_user.id, created_at=created_at, updated_at=updated_at
    )
    response = client.put("/todolists/1", json=todolist_data, headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated TodoList",
        "user_id": mock_current_user.id,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:30:00"
    }
    mock_todolist_repo.update_todo.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todolist_success(client, override_dependencies, mock_todolist_repo, mock_current_user):
    mock_todolist_repo.delete_todo.return_value = None
    response = client.delete("/todolists/1", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 204
    assert response.text == ""
    mock_todolist_repo.delete_todo.assert_called_once_with(1)
