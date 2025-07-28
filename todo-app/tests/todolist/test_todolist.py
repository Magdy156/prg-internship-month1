import pytest

def test_create_todolist(client, base_url, auth_headers):
    todolist_data = {"title": "Test TodoList"}
    response = client.post(f"{base_url}/todolists/", json=todolist_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == todolist_data["title"]

def test_read_todolist(client, base_url, created_todolist, auth_headers):
    todolist_id = created_todolist["id"]
    response = client.get(f"{base_url}/todolists/{todolist_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == created_todolist["title"]

def test_update_todolist(client, base_url, created_todolist, auth_headers):
    todolist_id = created_todolist["id"]
    update_todolist_data = {"title": "Updated TodoList"}
    response = client.put(f"{base_url}/todolists/{todolist_id}", json=update_todolist_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == update_todolist_data["title"]

def test_delete_todolist(client, base_url, created_todolist, auth_headers):
    todolist_id = created_todolist["id"]
    response = client.delete(f"{base_url}/todolists/{todolist_id}", headers=auth_headers)
    assert response.status_code == 204
