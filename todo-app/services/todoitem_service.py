from fastapi import Depends
from sqlalchemy.orm import Session
from dal.repositories.todoitem_repository import TodoItemRepository
from schemas.todoitem import TodoItemCreate
from models.todoitem import TodoItem
from db.database import get_db

class TodoItemService:
    def __init__(self, db: Session = Depends(get_db)):
        self.todoitem_repo = TodoItemRepository(db)

    def create_todo_item(self, todo_item: TodoItemCreate, todolist_id: int) -> TodoItem:
        return self.todoitem_repo.create_todo_item(todo_item, todolist_id)

    def get_todo_item(self, todo_item_id: int) -> TodoItem:
        return self.todoitem_repo.get_todo_item(todo_item_id)

    def update_todo_item(self, todo_item_id: int, todo_item: TodoItemCreate) -> TodoItem:
        return self.todoitem_repo.update_todo_item(todo_item_id, todo_item)

    def delete_todo_item(self, todo_item_id: int):
        self.todoitem_repo.delete_todo_item(todo_item_id)
        return {"detail": "TodoItem deleted"}
