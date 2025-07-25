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

    # Todo CRUD
    print("\nTesting Todo CRUD...")
    todo_data = {"title": "Test Todo"}
    response = requests.post(f"{BASE_URL}/todos/", json=todo_data, headers=headers)
    print(f"Create Todo - Status Code: {response.status_code}")
    print(f"Create Todo - Response: {response.text}")
    created_todo = response.json()
    print(f"Created Todo: {created_todo}")

    print(f"Sending headers for todo read: {headers}")
    response = requests.get(f"{BASE_URL}/todos/{created_todo['id']}", headers=headers)
    print(f"Read Todo - Status Code: {response.status_code}")
    print(f"Read Todo - Response: {response.text}")
    print(f"Read Todo: {response.json()}")

    update_todo_data = {"title": "Updated Todo"}
    print(f"Sending headers for todo update: {headers}")
    response = requests.put(f"{BASE_URL}/todos/{created_todo['id']}", json=update_todo_data, headers=headers)
    print(f"Update Todo - Status Code: {response.status_code}")
    print(f"Update Todo - Response: {response.text}")
    print(f"Updated Todo: {response.json()}")

    # TodoItem CRUD
    print("\nTesting TodoItem CRUD...")
    todo_item_data = {
        "title": "Test Item",
        "description": "Test Description",
        "completed": False,
        "priority": "MEDIUM",
        "todo_id": created_todo["id"]
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
        "todo_id": created_todo["id"]
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
