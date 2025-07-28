import pytest

def test_read_user(client, base_url, test_user, auth_headers):
    user_id = test_user["id"]
    response = client.get(f"{base_url}/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]
    assert response.json()["email"] == test_user["email"]

def test_update_user(client, base_url, test_user, auth_headers):
    user_id = test_user["id"]
    timestamp = test_user["username"].split("_")[1]
    update_user_data = {
        "username": f"updateduser_{timestamp}",
        "email": f"updated_{timestamp}@example.com",
        "password": "newpassword"
    }
    response = client.put(f"{base_url}/users/{user_id}", json=update_user_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == update_user_data["username"]
    assert response.json()["email"] == update_user_data["email"]

def test_login_after_update(client, base_url, test_user, auth_headers):
    user_id = test_user["id"]
    timestamp = test_user["username"].split("_")[1]
    update_user_data = {
        "username": f"updateduser_{timestamp}",
        "email": f"updated_{timestamp}@example.com",
        "password": "newpassword"
    }
    response = client.put(f"{base_url}/users/{user_id}", json=update_user_data, headers=auth_headers)
    assert response.status_code == 200

    login_data = {"username": update_user_data["username"], "password": update_user_data["password"]}
    response = client.post(
        f"{base_url}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_delete_user(client, base_url, test_user, auth_headers):
    user_id = test_user["id"]
    response = client.delete(f"{base_url}/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"
