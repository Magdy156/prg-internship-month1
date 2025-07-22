import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_crud():
    # Test User CRUD
    print("Testing User CRUD...")
    user_data = {
        "username": "another",
        "email": "testanother@example.com",
        "password": "testpassword"
    }

    # Create User
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    assert response.status_code == 200, f"Create User failed: {response.text}"
    user = response.json()
    user_id = user["id"]
    print(f"Created User: {user}")

    # Read User
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200, f"Read User failed: {response.text}"
    print(f"Read User: {response.json()}")

    # Update User
    updated_user = {
        "username": "updateduseranother",
        "email": "updated@example.com",
        "password": "newpassword_another"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=updated_user)
    assert response.status_code == 200, f"Update User failed: {response.text}"
    print(f"Updated User: {response.json()}")


if __name__ == "__main__":
    try:
        test_crud()
        print("\nAll CRUD tests passed successfully!")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")