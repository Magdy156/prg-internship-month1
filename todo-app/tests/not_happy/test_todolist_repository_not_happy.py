import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from dal.repositories.todolist_repository import TodoListRepository
from schemas.todolist import TodoListCreate, TodoListUpdate
from utils.exceptions import TodoListNotFoundException

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
async def test_get_todo_not_found(mock_db_session):
    repo = TodoListRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(TodoListNotFoundException):
        repo.get_todo(999)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_update_todo_not_found(mock_db_session):
    repo = TodoListRepository(mock_db_session)
    todolist_data = TodoListUpdate(
        title="Updated TodoList",
        user_id=1
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(TodoListNotFoundException):
        repo.update_todo(999, todolist_data)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todo_not_found(mock_db_session):
    repo = TodoListRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(TodoListNotFoundException):
        repo.delete_todo(999)
    mock_db_session.query.assert_called_once()
