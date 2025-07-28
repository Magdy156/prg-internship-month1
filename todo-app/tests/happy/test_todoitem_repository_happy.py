import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from dal.repositories.todoitem_repository import TodoItemRepository
from models.todoitem import TodoItem, Priority
from schemas.todoitem import TodoItemCreate, TodoItemUpdate, TodoItemResponse
from datetime import datetime, timezone

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
@patch("dal.repositories.todoitem_repository.datetime")
async def test_create_todo_item_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 28, 18, 25, tzinfo=timezone.utc)
    repo = TodoItemRepository(mock_db_session)
    todoitem_data = TodoItemCreate(
        title="Test Item",
        todolist_id=1,
        description="Test description",
        priority="MEDIUM",
        completed=False
    )
    mock_todolist_query = MagicMock()
    mock_todolist_query.filter.return_value.first.return_value = True
    mock_db_session.query.return_value = mock_todolist_query
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: setattr(obj, "id", 1)
    created_at = datetime(2025, 7, 28, 18, 25, tzinfo=timezone.utc)
    expected = TodoItemResponse(
        id=1,
        title="Test Item",
        todolist_id=1,
        description="Test description",
        priority=Priority.MEDIUM,
        completed=False,
        created_at=created_at,
        updated_at=created_at,
        due_date=None,
        category=None
    )
    result = repo.create_todo_item(todoitem_data, todolist_id=1)
    assert result == expected
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_get_todo_item_success(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    created_at = datetime(2025, 7, 28, 18, 25, tzinfo=timezone.utc)
    mock_todoitem = TodoItem(
        id=1,
        title="Test Item",
        todolist_id=1,
        description="Test description",
        priority="MEDIUM",
        completed=False,
        created_at=created_at,
        updated_at=created_at
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_todoitem
    mock_db_session.query.return_value = mock_query
    result = repo.get_todo_item(1)
    expected = TodoItemResponse(
        id=1,
        title="Test Item",
        todolist_id=1,
        description="Test description",
        priority=Priority.MEDIUM,
        completed=False,
        created_at=created_at,
        updated_at=created_at,
        due_date=None,
        category=None
    )
    assert result == expected
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
@patch("dal.repositories.todoitem_repository.datetime")
async def test_update_todo_item_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 28, 18, 30, tzinfo=timezone.utc)
    repo = TodoItemRepository(mock_db_session)
    todoitem_data = TodoItemUpdate(
        title="Updated Item",
        todolist_id=1,
        description="Updated description",
        priority=Priority.HIGH,
        completed=True
    )
    created_at = datetime(2025, 7, 28, 18, 25, tzinfo=timezone.utc)
    updated_at = datetime(2025, 7, 28, 18, 30, tzinfo=timezone.utc)
    mock_todoitem = TodoItem(
        id=1,
        title="Test Item",
        todolist_id=1,
        description="Test description",
        priority="MEDIUM",
        completed=False,
        created_at=created_at,
        updated_at=created_at
    )
    mock_todoitem_query = MagicMock()
    mock_todoitem_query.filter.return_value.first.return_value = mock_todoitem
    mock_todoitem_query.filter.return_value.update.return_value = 1
    mock_db_session.query.return_value = mock_todoitem_query
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: obj.__dict__.update(
        title=todoitem_data.title,
        description=todoitem_data.description,
        priority=todoitem_data.priority.value,
        completed=todoitem_data.completed,
        updated_at=updated_at
    )
    result = repo.update_todo_item(1, todoitem_data)
    expected = TodoItemResponse(
        id=1,
        title="Updated Item",
        todolist_id=1,
        description="Updated description",
        priority=Priority.HIGH,
        completed=True,
        created_at=created_at,
        updated_at=updated_at,
        due_date=None,
        category=None
    )
    assert result == expected
    mock_db_session.commit.assert_called_once()
    mock_db_session.query.assert_called()

@pytest.mark.asyncio
async def test_delete_todo_item_success(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    mock_todoitem = TodoItem(id=1, title="Test Item", todolist_id=1)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_todoitem
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete.return_value = None
    mock_db_session.commit.return_value = None
    repo.delete_todo_item(1)
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
