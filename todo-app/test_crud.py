import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_crud():
    # User CRUD
    print("Testing User CRUD...")
    user_data = {
        "username": f"another_{int(datetime.now().timestamp())}",
        "email": f"testanother_{int(datetime.now().timestamp())}@example.com",
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Create User - Status Code: {response.status_code}")
    print(f"Create User - Response: {response.text}")
    created_user = response.json()
    print(f"Created User: {created_user}")

    # Login
    print(f"Attempting login for {user_data['username']}")
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Login - Status Code: {response.status_code}")
    print(f"Login - Response: {response.text}")
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Sending headers for user read: {headers}")

    # Read User
    response = requests.get(f"{BASE_URL}/users/{created_user['id']}", headers=headers)
    print(f"Read User - Status Code: {response.status_code}")
    print(f"Read User - Response: {response.text}")
    print(f"Read User: {response.json()}")

    # Update User
    update_user_data = {
        "username": f"updateduser{user_data['username']}",
        "email": f"updated_{int(datetime.now().timestamp())}@example.com",
        "password": "newpassword"
    }
    response = requests.put(f"{BASE_URL}/users/{created_user['id']}", json=update_user_data, headers=headers)
    print(f"Update User - Status Code: {response.status_code}")
    print(f"Update User - Response: {response.text}")
    print(f"Updated User: {response.json()}")

    # Login after update
    print(f"Attempting login for {update_user_data['username']}")
    login_data = {"username": update_user_data["username"], "password": update_user_data["password"]}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Login - Status Code: {response.status_code}")
    print(f"Login - Response: {response.text}")
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"New token after update: {token}")

    # TodoList CRUD
    print("\nTesting TodoList CRUD...")
    todolist_data = {"title": "Test TodoList"}
    response = requests.post(f"{BASE_URL}/todolists/", json=todolist_data, headers=headers)
    print(f"Create TodoList - Status Code: {response.status_code}")
    print(f"Create TodoList - Response: {response.text}")
    created_todolist = response.json()
    print(f"Created TodoList: {created_todolist}")

    print(f"Sending headers for todolist read: {headers}")
    response = requests.get(f"{BASE_URL}/todolists/{created_todolist['id']}", headers=headers)
    print(f"Read TodoList - Status Code: {response.status_code}")
    print(f"Read TodoList - Response: {response.text}")
    print(f"Read TodoList: {response.json()}")

    update_todolist_data = {"title": "Updated TodoList"}
    print(f"Sending headers for todolist update: {headers}")
    response = requests.put(f"{BASE_URL}/todolists/{created_todolist['id']}", json=update_todolist_data, headers=headers)
    print(f"Update TodoList - Status Code: {response.status_code}")
    print(f"Update TodoList - Response: {response.text}")
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
    print(f"Sending headers for todoitem create: {headers}")
    response = requests.post(f"{BASE_URL}/todoitems/", json=todo_item_data, headers=headers)
    print(f"Create TodoItem - Status Code: {response.status_code}")
    print(f"Create TodoItem - Response: {response.text}")
    if response.status_code != 200:
        print(f"Test failed: Create TodoItem failed: {response.text}")
        raise Exception("Create TodoItem failed")
    created_todo_item = response.json()
    print(f"Created TodoItem: {created_todo_item}")

    print(f"Sending headers for todoitem read: {headers}")
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
    print(f"Sending headers for todoitem update: {headers}")
    response = requests.put(f"{BASE_URL}/todoitems/{created_todo_item['id']}", json=update_todo_item_data, headers=headers)
    print(f"Update TodoItem - Status Code: {response.status_code}")
    print(f"Update TodoItem - Response: {response.text}")
    if response.status_code != 200:
        print(f"Test failed: Update TodoItem failed: {response.text}")
        raise Exception("Update TodoItem failed")
    print(f"Updated TodoItem: {response.json()}")

    print(f"Sending headers for todoitem delete: {headers}")
    response = requests.delete(f"{BASE_URL}/todoitems/{created_todo_item['id']}", headers=headers)
    print(f"Delete TodoItem - Status Code: {response.status_code}")
    print(f"Delete TodoItem - Response: {response.text}")
    if response.status_code != 204:
        print(f"Test failed: Delete TodoItem failed: {response.text}")
        raise Exception("Delete TodoItem failed")

    print("All CRUD tests passed successfully!")

if __name__ == "__main__":
    try:
        test_crud()
    except Exception as e:
        print(f"Test failed: {str(e)}")
