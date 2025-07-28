import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from dal.repositories.todoitem_repository import TodoItemRepository
from schemas.todoitem import TodoItemCreate
from utils.exceptions import TodoItemNotFoundException, TodoListNotFoundException

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
async def test_create_todo_item_todolist_not_found(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    todoitem_data = TodoItemCreate(
        title="Test Item",
        todolist_id=999,
        description="Test description",
        priority="MEDIUM",
        completed=False
    )
    mock_todolist_query = MagicMock()
    mock_todolist_query.filter.return_value.first.return_value = None  # Simulate todolist not found
    mock_db_session.query.return_value = mock_todolist_query
    with pytest.raises(TodoListNotFoundException):
        repo.create_todo_item(todoitem_data, todolist_id=999)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_get_todo_item_not_found(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(TodoItemNotFoundException):
        repo.get_todo_item(999)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_update_todo_item_not_found(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    todoitem_data = TodoItemCreate(
        title="Updated Item",
        todolist_id=1,
        description="Updated description",
        priority="HIGH",
        completed=True
    )
    mock_todoitem_query = MagicMock()
    mock_todoitem_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_todoitem_query
    with pytest.raises(TodoItemNotFoundException):
        repo.update_todo_item(999, todoitem_data)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_delete_todo_item_not_found(mock_db_session):
    repo = TodoItemRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(TodoItemNotFoundException):
        repo.delete_todo_item(999)
    mock_db_session.query.assert_called_once()
