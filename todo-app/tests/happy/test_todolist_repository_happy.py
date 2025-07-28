import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from dal.repositories.todolist_repository import TodoListRepository
from models.todolist import TodoList
from schemas.todolist import TodoListCreate, TodoListUpdate, TodoListResponse
from datetime import datetime, timezone

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
@patch("dal.repositories.todolist_repository.datetime")
async def test_create_todo_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    repo = TodoListRepository(mock_db_session)
    todolist_data = TodoListCreate(
        title="Test TodoList",
        user_id=1
    )
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: setattr(obj, "id", 1)
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    expected = TodoListResponse(
        id=1,
        title="Test TodoList",
        user_id=1,
        created_at=created_at,
        updated_at=created_at
    )
    result = repo.create_todo(todolist_data, user_id=1)
    assert result == expected
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_get_todo_success(mock_db_session):
    repo = TodoListRepository(mock_db_session)
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    mock_todolist = TodoList(
        id=1,
        title="Test TodoList",
        user_id=1,
        created_at=created_at,
        updated_at=created_at
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_todolist
    mock_db_session.query.return_value = mock_query
    result = repo.get_todo(1)
    expected = TodoListResponse(
        id=1,
        title="Test TodoList",
        user_id=1,
        created_at=created_at,
        updated_at=created_at
    )
    assert result == expected
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
@patch("dal.repositories.todolist_repository.datetime")
async def test_update_todo_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 29, 12, 45, tzinfo=timezone.utc)
    repo = TodoListRepository(mock_db_session)
    todolist_data = TodoListUpdate(
        title="Updated TodoList"
    )
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    updated_at = datetime(2025, 7, 29, 12, 45, tzinfo=timezone.utc)
    mock_todolist = TodoList(
        id=1,
        title="Test TodoList",
        user_id=1,
        created_at=created_at,
        updated_at=created_at
    )
    mock_todolist_query = MagicMock()
    mock_todolist_query.filter.return_value.first.return_value = mock_todolist
    mock_todolist_query.filter.return_value.update.return_value = 1
    mock_db_session.query.return_value = mock_todolist_query
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: obj.__dict__.update(
        title=todolist_data.title,
        updated_at=updated_at
    )
    result = repo.update_todo(1, todolist_data)
    expected = TodoListResponse(
        id=1,
        title="Updated TodoList",
        user_id=1,
        created_at=created_at,
        updated_at=updated_at
    )
    assert result == expected
    mock_db_session.commit.assert_called_once()
    mock_db_session.query.assert_called()

@pytest.mark.asyncio
async def test_delete_todo_success(mock_db_session):
    repo = TodoListRepository(mock_db_session)
    mock_todolist = TodoList(id=1, title="Test TodoList", user_id=1)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_todolist
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete.return_value = None
    mock_db_session.commit.return_value = None
    repo.delete_todo(1)
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
