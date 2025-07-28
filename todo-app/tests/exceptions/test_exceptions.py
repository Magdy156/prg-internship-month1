import pytest

def test_read_non_existent_user(client, base_url, auth_headers):
    non_existent_user_id = 9999
    response = client.get(f"{base_url}/users/{non_existent_user_id}", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_login_invalid_password(client, base_url, test_user):
    invalid_login_data = {"username": test_user["username"], "password": "wrongpassword"}
    response = client.post(
        f"{base_url}/auth/login",
        data=invalid_login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401, f"Login with invalid password failed: {response.json()}"
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_non_existent_username(client, base_url, test_user):
    timestamp = test_user["username"].split("_")[1]
    invalid_login_data = {"username": f"nonexistent_{timestamp}", "password": "testpassword"}
    response = client.post(
        f"{base_url}/auth/login",
        data=invalid_login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 404, f"Login with non-existent username failed: {response.json()}"
    assert response.json()["detail"] == "User not found"

def test_invalid_jwt_token(client, base_url, test_user):
    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get(f"{base_url}/users/{test_user['id']}", headers=invalid_headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
