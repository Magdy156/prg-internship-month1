import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from dal.repositories.user_repository import UserRepository
from models.user import User
from schemas.user import UserCreateResponse, UserUpdateResponse
from datetime import datetime, timezone

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.mark.asyncio
async def test_get_user_by_id_success(mock_db_session):
    repo = UserRepository(mock_db_session)
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        created_at=created_at
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_db_session.query.return_value = mock_query
    result = repo.get_user_by_id(1)
    assert result == mock_user
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_by_username_success(mock_db_session):
    repo = UserRepository(mock_db_session)
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        created_at=created_at
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_db_session.query.return_value = mock_query
    result = repo.get_user_by_username("testuser")
    assert result == mock_user
    mock_db_session.query.assert_called_once()

@pytest.mark.asyncio
@patch("dal.repositories.user_repository.datetime")
async def test_create_user_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    repo = UserRepository(mock_db_session)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "hashed_password"
    }
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: setattr(obj, "id", 1)
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    expected = UserCreateResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=created_at
    )
    result = repo.create_user(user_data)
    assert result == expected
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
@patch("dal.repositories.user_repository.datetime")
async def test_update_user_success(mock_datetime, mock_db_session):
    mock_datetime.now.return_value = datetime(2025, 7, 29, 12, 45, tzinfo=timezone.utc)
    repo = UserRepository(mock_db_session)
    user_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "password": "new_hashed_password"
    }
    created_at = datetime(2025, 7, 29, 12, 44, tzinfo=timezone.utc)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        created_at=created_at
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_query.filter.return_value.update.return_value = 1
    mock_db_session.query.return_value = mock_query
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: obj.__dict__.update(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"]
    )
    result = repo.update_user(1, user_data)
    expected = UserUpdateResponse(
        id=1,
        username="updateduser",
        email="updated@example.com",
        created_at=created_at
    )
    assert result == expected
    mock_db_session.commit.assert_called_once()
    mock_db_session.query.assert_called()

@pytest.mark.asyncio
async def test_delete_user_success(mock_db_session):
    repo = UserRepository(mock_db_session)
    mock_user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed_password"
    )
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete.return_value = None
    mock_db_session.commit.return_value = None
    repo.delete_user(1)
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
