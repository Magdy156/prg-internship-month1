import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.user import User
from models.todolist import TodoList
from models.todoitem import TodoItem
from main import app
from db.database import SessionLocal, Base, engine
from passlib.context import CryptContext
from datetime import datetime
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def base_url():
    return "http://127.0.0.1:8000"

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def user_data():
    timestamp = int(datetime.now().timestamp())
    return {
        "username": f"test_user_{timestamp}",
        "email": f"test_{timestamp}@test.com",
        "password": "testpassword"
    }

@pytest.fixture(scope="function")
def test_user(db: Session, client: TestClient, base_url, user_data):
    # Create user via API
    response = client.post(f"{base_url}/auth/register", json=user_data)
    print(f"Register response: {response.status_code}, {response.json()}")  # Debug log
    if response.status_code != 200:
        # Clean up existing user if duplicate
        db.execute(text("DELETE FROM users WHERE username = :username"), {"username": user_data["username"]})
        db.commit()
        response = client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Failed to create user: {response.json()}"
    user = response.json()
    # Explicitly commit and start new session
    db.commit()
    new_db = SessionLocal()
    try:
        db_user = new_db.query(User).filter(User.username == user_data["username"]).first()
        if db_user:
            new_db.refresh(db_user)
        assert db_user, f"User {user_data['username']} not found in new session"
        print(f"Created user: {user}, DB user ID: {db_user.id}, DB username: {db_user.username}")  # Debug log
    finally:
        new_db.close()
    yield user
    # Cleanup: Delete all todoitems and todolists
    try:
        # Log remaining todolists
        remaining_todolists = db.execute(text("SELECT id, user_id FROM todolists")).fetchall()
        print(f"Remaining todolists before cleanup: {[(row.id, row.user_id) for row in remaining_todolists]}")  # Debug log
        db.execute(text("DELETE FROM todoitems"))
        db.execute(text("DELETE FROM todolists"))
        db.commit()
        print(f"Cleaned up all todolists and todoitems for user {user['id']}")  # Debug log
    except Exception as e:
        print(f"Failed to clean up todolists/todoitems for user {user['id']}: {e}")
    # Delete user
    login_data = {"username": user_data["username"], "password": "testpassword"}
    response = client.post(f"{base_url}/auth/login", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(f"Cleanup login response: {response.status_code}, {response.json()}")  # Debug log
    if response.status_code == 200:
        token = response.json().get("access_token")
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.delete(f"{base_url}/users/{user['id']}", headers=headers)
            print(f"Cleanup delete response: {response.status_code}, {response.json()}")  # Debug log
    # Fallback cleanup
    try:
        db.execute(text("DELETE FROM users WHERE id = :id"), {"id": user["id"]})
        db.commit()
        print(f"Cleaned up user {user['id']}")  # Debug log
    except Exception as e:
        print(f"Cleanup failed for user {user['id']}: {e}")

@pytest.fixture
def auth_headers(client: TestClient, test_user, base_url, db: Session):
    login_data = {"username": test_user["username"], "password": "testpassword"}
    # Retry login with new session
    token = None
    for attempt in range(3):
        new_db = SessionLocal()
        try:
            db_user = new_db.query(User).filter(User.username == test_user["username"]).first()
            if db_user:
                new_db.refresh(db_user)
            print(f"User check before login (attempt {attempt + 1}): {db_user}")  # Debug log
        finally:
            new_db.close()
        response = client.post(f"{base_url}/auth/login", data=login_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(f"Login response in auth_headers (attempt {attempt + 1}): {response.status_code}, {response.json()}")  # Debug log
        if response.status_code == 200:
            token = response.json().get("access_token")
            if token:
                break
        # Commit main session
        db.commit()
    assert token, f"Login failed after 3 attempts: {response.json()}"
    # Verify user in new session
    new_db = SessionLocal()
    try:
        db_user = new_db.query(User).filter(User.username == test_user["username"]).first()
        assert db_user, f"User {test_user['username']} not found in new session during auth_headers"
        print(f"User ID from database: {db_user.id}, from API: {test_user['id']}")  # Debug log
    finally:
        new_db.close()
    # Decode JWT token
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        print(f"Decoded JWT token: {decoded_token}")  # Debug log
        assert "sub" in decoded_token, "JWT token missing 'sub' claim"
        print(f"JWT token sub: {decoded_token['sub']}, expected username: {test_user['username']}")  # Debug log
    except Exception as e:
        print(f"Failed to decode JWT token: {e}")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Sending headers: {headers}")  # Debug log
    # Test token with /users/me endpoint
    response = client.get(f"{base_url}/users/me", headers=headers)
    print(f"Users/me response with token: {response.status_code}, {response.json()}")  # Debug log
    return headers

@pytest.fixture
def refresh_token(client, base_url, test_user):
    login_data = {"username": test_user["username"], "password": "testpassword"}
    response = client.post(
        f"{base_url}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Login response in refresh_token: {response.status_code}, {response.json()}")  # Debug log
    assert response.status_code == 200, f"Login failed for refresh_token: {response.json()}"
    return response.json().get("refresh_token")

@pytest.fixture
def created_todolist(client: TestClient, auth_headers: dict, test_user, db: Session, base_url):
    todolist_data = {"title": "Test TodoList"}  # Rely on JWT for user_id
    response = client.post(f"{base_url}/todolists/", json=todolist_data, headers=auth_headers)
    print(f"Todolist creation response: {response.status_code}, {response.json()}")  # Debug log
    assert response.status_code == 200, f"Failed to create TodoList: {response.json()}"
    todolist = response.json()
    yield todolist
    # Robust cleanup in new session
    new_db = SessionLocal()
    try:
        # Delete associated todoitems first
        new_db.execute(text("DELETE FROM todoitems WHERE todolist_id = :id"), {"id": todolist["id"]})
        new_db.execute(text("DELETE FROM todolists WHERE id = :id"), {"id": todolist["id"]})
        new_db.commit()
        print(f"Cleaned up todolist {todolist['id']} and its todoitems")  # Debug log
    except Exception as e:
        print(f"Cleanup failed for todolist {todolist['id']}: {e}")
    finally:
        new_db.close()

@pytest.fixture
def created_todoitem(client: TestClient, auth_headers: dict, created_todolist, db: Session, base_url):
    todoitem_data = {
        "title": "Test Item",
        "description": "Test Description",
        "completed": False,
        "priority": "MEDIUM",
        "todolist_id": created_todolist["id"]
    }
    response = client.post(f"{base_url}/todoitems/", json=todoitem_data, headers=auth_headers)
    print(f"Todoitem creation response: {response.status_code}, {response.json()}")  # Debug log
    assert response.status_code == 200, f"Failed to create TodoItem: {response.json()}"
    todoitem = response.json()
    yield todoitem
    # Robust cleanup
    try:
        db.execute(text("DELETE FROM todoitems WHERE id = :id"), {"id": todoitem["id"]})
        db.commit()
        print(f"Cleaned up todoitem {todoitem['id']}")  # Debug log
    except Exception as e:
        print(f"Cleanup failed for todoitem {todoitem['id']}: {e}")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    from db.database import Base, engine
    # Ensure all tables are created
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up data without dropping tables
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todoitems"))
        conn.execute(text("DELETE FROM todolists"))
        conn.execute(text("DELETE FROM users"))
        conn.commit()
        print("Cleaned up all tables in setup_database")  # Debug log
