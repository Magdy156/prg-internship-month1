import pytest
from fastapi.testclient import TestClient
from schemas.todoitem import TodoItemCreate, TodoItemResponse
from models.user import User
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_todoitem_success(client, override_dependencies, mock_todoitem_repo, mock_todolist_repo, mock_current_user):
    todoitem_data = {"title": "Test TodoItem", "todolist_id": 1, "description": "Test description", "priority": "MEDIUM", "completed": False}
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    mock_todolist_repo.get_todo.return_value = True  # Simulate todolist exists
    mock_todoitem_repo.create_todo_item.return_value = TodoItemResponse(
        id=1, title="Test TodoItem", description="Test description", completed=False, priority="MEDIUM",
        todolist_id=1, created_at=created_at, updated_at=created_at
    )
    response = client.post("/todoitems/", json=todoitem_data, headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test TodoItem",
        "description": "Test description",
        "completed": False,
        "priority": "MEDIUM",
        "todolist_id": 1,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:25:00",
        "due_date": None,
        "category": None
    }
    mock_todoitem_repo.create_todo_item.assert_called_once()

@pytest.mark.asyncio
async def test_read_todoitem_success(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    mock_todoitem_repo.get_todo_item.return_value = TodoItemResponse(
        id=1, title="Test TodoItem", description="Test description", completed=False, priority="MEDIUM",
        todolist_id=1, created_at=created_at, updated_at=created_at
    )
    response = client.get("/todoitems/1", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test TodoItem",
        "description": "Test description",
        "completed": False,
        "priority": "MEDIUM",
        "todolist_id": 1,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:25:00",
        "due_date": None,
        "category": None
    }
    mock_todoitem_repo.get_todo_item.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_todoitem_success(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    todoitem_data = {"title": "Updated TodoItem", "todolist_id": 1, "description": "Updated description", "priority": "HIGH", "completed": True}
    created_at = datetime.fromisoformat("2025-07-28T18:25:00")
    updated_at = datetime.fromisoformat("2025-07-28T18:30:00")
    mock_todoitem_repo.update_todo_item.return_value = TodoItemResponse(
        id=1, title="Updated TodoItem", description="Updated description", completed=True, priority="HIGH",
        todolist_id=1, created_at=created_at, updated_at=updated_at
    )
    response = client.put("/todoitems/1", json=todoitem_data, headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated TodoItem",
        "description": "Updated description",
        "completed": True,
        "priority": "HIGH",
        "todolist_id": 1,
        "created_at": "2025-07-28T18:25:00",
        "updated_at": "2025-07-28T18:30:00",
        "due_date": None,
        "category": None
    }
    mock_todoitem_repo.update_todo_item.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todoitem_success(client, override_dependencies, mock_todoitem_repo, mock_current_user):
    mock_todoitem_repo.delete_todo_item.return_value = None
    response = client.delete("/todoitems/1", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 204
    assert response.text == ""
    mock_todoitem_repo.delete_todo_item.assert_called_once_with(1)
