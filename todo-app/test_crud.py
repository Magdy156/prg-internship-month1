import requests
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000"

def test_crud():
    try:
        # User CRUD
        print("Testing User CRUD...")
        timestamp = int(datetime.now(timezone.utc).timestamp())
        user_data = {
            "username": f"testuser_{timestamp}",
            "email": f"testuser_{timestamp}@example.com",
            "password": "testpassword"
        }

        # Register
        print(f"Registering user: {user_data['username']}")
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Register User - Status Code: {response.status_code}")
        print(f"Register User - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Register User failed: {response.text}")
            raise Exception("Register User failed")
        created_user = response.json()
        print(f"Created User: {created_user}")

        # Test UsernameExistsException
        print("Testing register with existing username...")
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Register Existing User - Status Code: {response.status_code}")
        print(f"Register Existing User - Response: {response.text}")
        if response.status_code != 400 or response.json().get("detail") != "Username already exists":
            print(f"Test failed: Expected 400 with 'Username already exists', got {response.status_code}: {response.text}")
            raise Exception("UsernameExistsException test failed")

        # Login
        print(f"Attempting login for {user_data['username']}")
        login_data = {"username": user_data["username"], "password": "testpassword"}
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login - Status Code: {response.status_code}")
        print(f"Login - Response: {response.text}")
        if response.status_code != 200 or "access_token" not in response.json():
            print(f"Test failed: Login failed: {response.text}")
            raise Exception("Login failed")
        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"Access Token: {access_token[:10]}...")

        # Test Validate Token
        print("Testing validate token...")
        response = requests.post(f"{BASE_URL}/auth/validate-token", headers=headers)
        print(f"Validate Token - Status Code: {response.status_code}")
        print(f"Validate Token - Response: {response.text}")
        if response.status_code != 200 or response.json().get("username") != user_data["username"]:
            print(f"Test failed: Validate Token failed: {response.text}")
            raise Exception("Validate Token failed")
        print(f"Validated User: {response.json()}")

        # Test Invalid Token
        print("Testing invalid token validation...")
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        response = requests.post(f"{BASE_URL}/auth/validate-token", headers=invalid_headers)
        print(f"Invalid Token - Status Code: {response.status_code}")
        print(f"Invalid Token - Response: {response.text}")
        if response.status_code != 401 or response.json().get("detail") != "Could not validate credentials":
            print(f"Test failed: Expected 401 with 'Could not validate credentials', got {response.status_code}: {response.text}")
            raise Exception("JWTDecodeException test failed (invalid token)")

        # Test Refresh Token
        print("Testing refresh token...")
        response = requests.post(f"{BASE_URL}/auth/refresh?refresh_token={refresh_token}")
        print(f"Refresh Token - Status Code: {response.status_code}")
        print(f"Refresh Token - Response: {response.text}")
        if response.status_code != 200 or "access_token" not in response.json():
            print(f"Test failed: Refresh Token failed: {response.text}")
            raise Exception("Refresh Token failed")
        new_access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {new_access_token}"}
        print(f"New Access Token: {new_access_token[:10]}...")

        # Test Invalid Refresh Token
        print("Testing invalid refresh token...")
        invalid_refresh_token = "invalid.refresh.token"
        response = requests.post(f"{BASE_URL}/auth/refresh?refresh_token={invalid_refresh_token}")
        print(f"Invalid Refresh Token - Status Code: {response.status_code}")
        print(f"Invalid Refresh Token - Response: {response.text}")
        if response.status_code != 401 or response.json().get("detail") != "Could not validate credentials":
            print(f"Test failed: Expected 401 with 'Could not validate credentials', got {response.status_code}: {response.text}")
            raise Exception("JWTDecodeException test failed (invalid refresh token)")

        # Read User
        print(f"Reading user ID {created_user['id']}")
        response = requests.get(f"{BASE_URL}/users/{created_user['id']}", headers=headers)
        print(f"Read User - Status Code: {response.status_code}")
        print(f"Read User - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Read User failed: {response.text}")
            raise Exception("Read User failed")
        print(f"Read User: {response.json()}")

        # TodoList CRUD
        print("\nTesting TodoList CRUD...")
        todolist_data = {"title": "Test TodoList"}
        response = requests.post(f"{BASE_URL}/todolists/", json=todolist_data, headers=headers)
        print(f"Create TodoList - Status Code: {response.status_code}")
        print(f"Create TodoList - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Create TodoList failed: {response.text}")
            raise Exception("Create TodoList failed")
        created_todolist = response.json()
        print(f"Created TodoList: {created_todolist}")

        response = requests.get(f"{BASE_URL}/todolists/{created_todolist['id']}", headers=headers)
        print(f"Read TodoList - Status Code: {response.status_code}")
        print(f"Read TodoList - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Read TodoList failed: {response.text}")
            raise Exception("Read TodoList failed")
        print(f"Read TodoList: {response.json()}")

        update_todolist_data = {"title": "Updated TodoList"}
        response = requests.put(f"{BASE_URL}/todolists/{created_todolist['id']}", json=update_todolist_data, headers=headers)
        print(f"Update TodoList - Status Code: {response.status_code}")
        print(f"Update TodoList - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Update TodoList failed: {response.text}")
            raise Exception("Update TodoList failed")
        print(f"Updated TodoList: {response.json()}")

        # TodoItem CRUD
        print("\nTesting TodoItem CRUD...")
        todo_item_data = {
            "title": "Test Item",
            "description": "Test Description",
            "completed": False,
            "priority": "MEDIUM",
            "todolist_id": created_todolist["id"]
        }
        response = requests.post(f"{BASE_URL}/todoitems/", json=todo_item_data, headers=headers)
        print(f"Create TodoItem - Status Code: {response.status_code}")
        print(f"Create TodoItem - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Create TodoItem failed: {response.text}")
            raise Exception("Create TodoItem failed")
        created_todo_item = response.json()
        print(f"Created TodoItem: {created_todo_item}")

        response = requests.get(f"{BASE_URL}/todoitems/{created_todo_item['id']}", headers=headers)
        print(f"Read TodoItem - Status Code: {response.status_code}")
        print(f"Read TodoItem - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Read TodoItem failed: {response.text}")
            raise Exception("Read TodoItem failed")
        print(f"Read TodoItem: {response.json()}")

        update_todo_item_data = {
            "title": "Updated Item",
            "description": "Updated Description",
            "completed": True,
            "priority": "HIGH",
            "todolist_id": created_todolist["id"]
        }
        response = requests.put(f"{BASE_URL}/todoitems/{created_todo_item['id']}", json=update_todo_item_data, headers=headers)
        print(f"Update TodoItem - Status Code: {response.status_code}")
        print(f"Update TodoItem - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Update TodoItem failed: {response.text}")
            raise Exception("Update TodoItem failed")
        print(f"Updated TodoItem: {response.json()}")

        # Cleanup TodoItem and TodoList before updating user
        response = requests.delete(f"{BASE_URL}/todoitems/{created_todo_item['id']}", headers=headers)
        print(f"Delete TodoItem - Status Code: {response.status_code}")
        print(f"Delete TodoItem - Response: {response.text}")
        if response.status_code != 204:
            print(f"Test failed: Delete TodoItem failed: {response.text}")
            raise Exception("Delete TodoItem failed")

        response = requests.delete(f"{BASE_URL}/todolists/{created_todolist['id']}", headers=headers)
        print(f"Delete TodoList - Status Code: {response.status_code}")
        print(f"Delete TodoList - Response: {response.text}")
        if response.status_code != 204:
            print(f"Test failed: Delete TodoList failed: {response.text}")
            raise Exception("Delete TodoList failed")

        # Update User
        update_user_data = {
            "username": f"updateduser_{timestamp}",
            "email": f"updated_{timestamp}@example.com",
            "password": "newpassword"
        }
        print(f"Updating user ID {created_user['id']}")
        response = requests.put(f"{BASE_URL}/users/{created_user['id']}", json=update_user_data, headers=headers)
        print(f"Update User - Status Code: {response.status_code}")
        print(f"Update User - Response: {response.text}")
        if response.status_code != 200:
            print(f"Test failed: Update User failed: {response.text}")
            raise Exception("Update User failed")
        print(f"Updated User: {response.json()}")

        # Login after update
        print(f"Attempting login for {update_user_data['username']}")
        login_data = {"username": update_user_data["username"], "password": update_user_data["password"]}
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login After Update - Status Code: {response.status_code}")
        print(f"Login After Update - Response: {response.text}")
        if response.status_code != 200 or "access_token" not in response.json():
            print(f"Test failed: Login after update failed: {response.text}")
            raise Exception("Login after update failed")
        headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
        print(f"New Token After Update: {response.json()['access_token'][:10]}...")

        # Exception Tests
        print("\nTesting Exception Handling...")
        print("Testing read non-existent user...")
        non_existent_user_id = 9999
        response = requests.get(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
        print(f"Read Non-Existent User - Status Code: {response.status_code}")
        print(f"Read Non-Existent User - Response: {response.text}")
        if response.status_code != 404 or response.json().get("detail") != "User not found":
            print(f"Test failed: Expected 404 with 'User not found', got {response.status_code}: {response.text}")
            raise Exception("UserNotFoundException test failed")

        print("Testing login with incorrect password...")
        invalid_login_data = {"username": update_user_data["username"], "password": "wrongpassword"}
        response = requests.post(f"{BASE_URL}/auth/login", data=invalid_login_data)
        print(f"Login Invalid Password - Status Code: {response.status_code}")
        print(f"Login Invalid Password - Response: {response.text}")
        if response.status_code != 401 or response.json().get("detail") != "Incorrect username or password":
            print(f"Test failed: Expected 401 with 'Incorrect username or password', got {response.status_code}: {response.text}")
            raise Exception("InvalidCredentialsException test failed")

        print("Testing login with non-existent username...")
        invalid_login_data = {"username": f"nonexistent_{timestamp}", "password": "testpassword"}
        response = requests.post(f"{BASE_URL}/auth/login", data=invalid_login_data)
        print(f"Login Non-Existent Username - Status Code: {response.status_code}")
        print(f"Login Non-Existent Username - Response: {response.text}")
        if response.status_code != 404 or response.json().get("detail") != "User not found":
            print(f"Test failed: Expected 404 with 'User not found', got {response.status_code}: {response.text}")
            raise Exception("UserNotFoundException test failed (login)")

        print("Testing invalid JWT token...")
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        response = requests.get(f"{BASE_URL}/users/{created_user['id']}", headers=invalid_headers)
        print(f"Read User with Invalid Token - Status Code: {response.status_code}")
        print(f"Read User with Invalid Token - Response: {response.text}")
        if response.status_code != 401 or response.json().get("detail") != "Could not validate credentials":
            print(f"Test failed: Expected 401 with 'Could not validate credentials', got {response.status_code}: {response.text}")
            raise Exception("JWTDecodeException test failed")

        # Delete User (Cleanup)
        print(f"Deleting user ID {created_user['id']}")
        response = requests.delete(f"{BASE_URL}/users/{created_user['id']}", headers=headers)
        print(f"Delete User - Status Code: {response.status_code}")
        print(f"Delete User - Response: {response.text}")
        if response.status_code != 200 or response.json().get("detail") != "User deleted":
            print(f"Test failed: Expected 200 with 'User deleted', got {response.status_code}: {response.text}")
            raise Exception("Delete User failed")

        print("All CRUD and exception tests passed successfully!")

    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_crud()
