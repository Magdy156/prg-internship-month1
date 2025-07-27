from fastapi import Depends
from schemas.todoitem import TodoItemCreate, TodoItemResponse
from dal.repositories.todoitem_repository import TodoItemRepository
from utils.dependencies import get_todoitem_repository

class TodoItemService:
    def __init__(self, todoitem_repo: TodoItemRepository = Depends(get_todoitem_repository)):
        self.todoitem_repo = todoitem_repo

    def create_todo_item(self, todo_item: TodoItemCreate, todolist_id: int) -> TodoItemResponse:
        return self.todoitem_repo.create_todo_item(todo_item, todolist_id)

    def get_todo_item(self, todo_item_id: int) -> TodoItemResponse:
        return self.todoitem_repo.get_todo_item(todo_item_id)

    def update_todo_item(self, todo_item_id: int, todo_item: TodoItemCreate) -> TodoItemResponse:
        return self.todoitem_repo.update_todo_item(todo_item_id, todo_item)

    def delete_todo_item(self, todo_item_id: int):
        self.todoitem_repo.delete_todo_item(todo_item_id)
        return {"detail": "TodoItem deleted"}
