import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from dal.repositories.user_repository import UserRepository
from utils.exceptions import UserNotFoundException

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(UserNotFoundException):
        repo.get_user_by_id(1)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_by_username_not_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(UserNotFoundException):
        repo.get_user_by_username("testuser")
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_not_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    user_data = {
        "username": "updateduser",
        "password": "new_hashed_password"
    }
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(UserNotFoundException):
        repo.update_user(1, user_data)
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_delete_user_not_found(mock_db_session):
    repo = UserRepository(mock_db_session)
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    with pytest.raises(UserNotFoundException):
        repo.delete_user(1)
    mock_db_session.query.assert_called_once()
