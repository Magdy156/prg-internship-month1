import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text

def test_register_user(client, base_url, user_data):
    response = client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Register failed: {response.json()}"
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]

def test_register_existing_user(client, base_url, user_data, test_user, db: Session):
    # Ensure no duplicate users exist before test
    db.execute(text("DELETE FROM users WHERE username = :username"), {"username": user_data["username"]})
    db.commit()
    # Re-create the user
    response = client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Failed to create user for test: {response.json()}"
    # Try registering the same user again
    response = client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 400, f"Expected 400 for duplicate user, got: {response.json()}"
    assert response.json()["detail"] == "Username already exists"

def test_login_user(client, base_url, test_user):
    login_data = {
        "username": test_user["username"],
        "password": "testpassword"
    }
    response = client.post(
        f"{base_url}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Login failed: {response.json()}"
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_refresh_token(client, base_url, refresh_token):
    response = client.post(f"{base_url}/auth/refresh?refresh_token={refresh_token}")
    assert response.status_code == 200, f"Refresh token failed: {response.json()}"
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_invalid_refresh_token(client, base_url):
    response = client.post(f"{base_url}/auth/refresh?refresh_token=invalid.refresh.token")
    assert response.status_code == 401, f"Invalid refresh token failed: {response.json()}"
    assert response.json()["detail"] == "Could not validate credentials"
