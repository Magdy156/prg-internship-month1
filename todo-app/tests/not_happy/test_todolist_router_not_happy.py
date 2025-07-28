import pytest
from fastapi.testclient import TestClient
from schemas.todolist import TodoListCreate
from utils.exceptions import TodoListNotFoundException
from jose import JWTError

@pytest.mark.asyncio
async def test_create_todolist_unauthorized(client, mock_auth_utils):
    _, _, decode_mock = mock_auth_utils
    decode_mock.side_effect = JWTError("Invalid token")
    todolist_data = {"title": "Test TodoList"}
    response = client.post("/todolists/", json=todolist_data, headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
    decode_mock.assert_called_once()

@pytest.mark.asyncio
async def test_read_todolist_unauthorized(client, mock_auth_utils):
    _, _, decode_mock = mock_auth_utils
    decode_mock.side_effect = JWTError("Invalid token")
    response = client.get("/todolists/1", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
    decode_mock.assert_called_once()

@pytest.mark.asyncio
async def test_read_todolist_not_found(client, override_dependencies, mock_todolist_repo, mock_current_user):
    mock_todolist_repo.get_todo.side_effect = TodoListNotFoundException
    response = client.get("/todolists/999", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoList not found"}
    mock_todolist_repo.get_todo.assert_called_once_with(999)

@pytest.mark.asyncio
async def test_update_todolist_not_found(client, override_dependencies, mock_todolist_repo, mock_current_user):
    mock_todolist_repo.update_todo.side_effect = TodoListNotFoundException
    todolist_data = {"title": "Updated TodoList"}
    response = client.put("/todolists/999", json=todolist_data, headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoList not found"}
    mock_todolist_repo.update_todo.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todolist_not_found(client, override_dependencies, mock_todolist_repo, mock_current_user):
    mock_todolist_repo.delete_todo.side_effect = TodoListNotFoundException
    response = client.delete("/todolists/999", headers={"Authorization": "Bearer mocked_access_token"})
    assert response.status_code == 404
    assert response.json() == {"detail": "TodoList not found"}
    mock_todolist_repo.delete_todo.assert_called_once_with(999)
