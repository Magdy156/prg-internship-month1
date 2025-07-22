import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_user_crud():
    print("Testing User CRUD...")
    # Use unique username and email to avoid conflicts
    timestamp = str(int(datetime.now().timestamp()))
    user_data = {
        "username": f"another_{timestamp}",
        "email": f"testanother_{timestamp}@example.com",
        "password": "testpassword"
    }

    # Create User
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data, timeout=5)
        print(f"Create User - Status Code: {response.status_code}")
        print(f"Create User - Response: {response.text}")
        assert response.status_code == 200, f"Create User failed: {response.text}"
        user = response.json()
        user_id = user["id"]
        print(f"Created User: {user}")
    except requests.exceptions.Timeout:
        print("Create User timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Create User request failed: {e}")
        raise

    # Read User
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}", timeout=5)
        print(f"Read User - Status Code: {response.status_code}")
        print(f"Read User - Response: {response.text}")
        assert response.status_code == 200, f"Read User failed: {response.text}"
        print(f"Read User: {response.json()}")
    except requests.exceptions.Timeout:
        print("Read User timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Read User request failed: {e}")
        raise

    # Update User
    updated_user = {
        "username": f"updateduseranother_{timestamp}",
        "email": f"updated_{timestamp}@example.com",
        "password": "newpassword_another"
    }
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=updated_user, timeout=5)
        print(f"Update User - Status Code: {response.status_code}")
        print(f"Update User - Response: {response.text}")
        assert response.status_code == 200, f"Update User failed: {response.text}"
        print(f"Updated User: {response.json()}")
    except requests.exceptions.Timeout:
        print("Update User timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Update User request failed: {e}")
        raise
    return user_id

def test_todo_crud(user_id):
    print("\nTesting Todo CRUD...")
    todo_data = {"title": "Test Todo"}
    try:
        response = requests.post(f"{BASE_URL}/todos/?user_id={user_id}", json=todo_data, timeout=5)
        print(f"Create Todo - Status Code: {response.status_code}")
        print(f"Create Todo - Response: {response.text}")
        assert response.status_code == 200, f"Create Todo failed: {response.text}"
        todo = response.json()
        todo_id = todo["id"]
        print(f"Created Todo: {todo}")
    except requests.exceptions.Timeout:
        print("Create Todo timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Create Todo request failed: {e}")
        raise

    # Read Todo
    try:
        response = requests.get(f"{BASE_URL}/todos/{todo_id}", timeout=5)
        print(f"Read Todo - Status Code: {response.status_code}")
        print(f"Read Todo - Response: {response.text}")
        assert response.status_code == 200, f"Read Todo failed: {response.text}"
        print(f"Read Todo: {response.json()}")
    except requests.exceptions.Timeout:
        print("Read Todo timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Read Todo request failed: {e}")
        raise

    # Update Todo
    updated_todo = {"title": "Updated Todo"}
    try:
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=updated_todo, timeout=5)
        print(f"Update Todo - Status Code: {response.status_code}")
        print(f"Update Todo - Response: {response.text}")
        assert response.status_code == 200, f"Update Todo failed: {response.text}"
        print(f"Updated Todo: {response.json()}")
    except requests.exceptions.Timeout:
        print("Update Todo timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Update Todo request failed: {e}")
        raise
    return todo_id

def test_todoitem_crud(todo_id):
    print("\nTesting TodoItem CRUD...")
    todo_item_data = {
        "title": "Test Item",
        "description": "Test Description",
        "completed": False,
        "priority": "medium",
        "todo_id": todo_id
    }
    try:
        response = requests.post(f"{BASE_URL}/todoitems/", json=todo_item_data, timeout=5)
        print(f"Create TodoItem - Status Code: {response.status_code}")
        print(f"Create TodoItem - Response: {response.text}")
        assert response.status_code == 200, f"Create TodoItem failed: {response.text}"
        todo_item = response.json()
        todo_item_id = todo_item["id"]
        print(f"Created TodoItem: {todo_item}")
    except requests.exceptions.Timeout:
        print("Create TodoItem timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Create TodoItem request failed: {e}")
        raise

    # Read TodoItem
    try:
        response = requests.get(f"{BASE_URL}/todoitems/{todo_item_id}", timeout=5)
        print(f"Read TodoItem - Status Code: {response.status_code}")
        print(f"Read TodoItem - Response: {response.text}")
        assert response.status_code == 200, f"Read TodoItem failed: {response.text}"
        print(f"Read TodoItem: {response.json()}")
    except requests.exceptions.Timeout:
        print("Read TodoItem timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Read TodoItem request failed: {e}")
        raise

    # Update TodoItem
    updated_todo_item = {
        "title": "Updated Item",
        "description": "Updated Description",
        "completed": True,
        "priority": "high",
        "todo_id": todo_id
    }
    try:
        response = requests.put(f"{BASE_URL}/todoitems/{todo_item_id}", json=updated_todo_item, timeout=5)
        print(f"Update TodoItem - Status Code: {response.status_code}")
        print(f"Update TodoItem - Response: {response.text}")
        assert response.status_code == 200, f"Update TodoItem failed: {response.text}"
        print(f"Updated TodoItem: {response.json()}")
    except requests.exceptions.Timeout:
        print("Update TodoItem timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Update TodoItem request failed: {e}")
        raise

    # Delete TodoItem
    try:
        response = requests.delete(f"{BASE_URL}/todoitems/{todo_item_id}", timeout=5)
        print(f"Delete TodoItem - Status Code: {response.status_code}")
        print(f"Delete TodoItem - Response: {response.text}")
        assert response.status_code == 200, f"Delete TodoItem failed: {response.text}"
        print(f"Deleted TodoItem: {response.json()}")
    except requests.exceptions.Timeout:
        print("Delete TodoItem timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Delete TodoItem request failed: {e}")
        raise

def test_crud():
    user_id = test_user_crud()
    todo_id = test_todo_crud(user_id)
    test_todoitem_crud(todo_id)
    # Delete Todo after TodoItem tests
    try:
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}", timeout=5)
        print(f"Final Delete Todo - Status Code: {response.status_code}")
        print(f"Final Delete Todo - Response: {response.text}")
        assert response.status_code == 200, f"Final Delete Todo failed: {response.text}"
        print(f"Final Deleted Todo: {response.json()}")
    except requests.exceptions.Timeout:
        print("Final Delete Todo timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Final Delete Todo request failed: {e}")
        raise
    # Delete User after all tests
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}", timeout=5)
        print(f"Final Delete User - Status Code: {response.status_code}")
        print(f"Final Delete User - Response: {response.text}")
        assert response.status_code == 200, f"Final Delete User failed: {response.text}"
        print(f"Final Deleted User: {response.json()}")
    except requests.exceptions.Timeout:
        print("Final Delete User timed out: Server not responding")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Final Delete User request failed: {e}")
        raise

if __name__ == "__main__":
    try:
        test_crud()
        print("\nAll CRUD tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
