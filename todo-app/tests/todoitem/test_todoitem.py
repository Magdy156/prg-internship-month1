import pytest

def test_create_todoitem(client, base_url, auth_headers, created_todolist):
    todo_item_data = {
        "title": "Test Item",
        "description": "Test Description",
        "completed": False,
        "priority": "MEDIUM",
        "todolist_id": created_todolist["id"]
    }
    response = client.post(f"{base_url}/todoitems/", json=todo_item_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == todo_item_data["title"]
    assert response.json()["todolist_id"] == created_todolist["id"]

def test_read_todoitem(client, base_url, created_todoitem, auth_headers):
    todoitem_id = created_todoitem["id"]
    response = client.get(f"{base_url}/todoitems/{todoitem_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == created_todoitem["title"]

def test_update_todoitem(client, base_url, created_todoitem, auth_headers, created_todolist):
    todoitem_id = created_todoitem["id"]
    update_todo_item_data = {
        "title": "Updated Item",
        "description": "Updated Description",
        "completed": True,
        "priority": "HIGH",
        "todolist_id": created_todolist["id"]
    }
    response = client.put(f"{base_url}/todoitems/{todoitem_id}", json=update_todo_item_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == update_todo_item_data["title"]
    assert response.json()["completed"] is True

def test_delete_todoitem(client, base_url, created_todoitem, auth_headers):
    todoitem_id = created_todoitem["id"]
    response = client.delete(f"{base_url}/todoitems/{todoitem_id}", headers=auth_headers)
    assert response.status_code == 204
