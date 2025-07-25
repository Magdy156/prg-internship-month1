from fastapi import Depends
from sqlalchemy.orm import Session
from dal.repositories.todo_repository import TodoRepository
from schemas.todo import TodoCreate, TodoResponse
from models.todo import Todo
from db.database import get_db

class TodoService:
    def __init__(self, db: Session = Depends(get_db)):
        self.todo_repo = TodoRepository(db)

    def create_todo(self, todo: TodoCreate, user_id: int) -> Todo:
        return self.todo_repo.create_todo(todo, user_id)

    def get_todo(self, todo_id: int) -> Todo:
        return self.todo_repo.get_todo(todo_id)

    def update_todo(self, todo_id: int, todo: TodoCreate) -> Todo:
        return self.todo_repo.update_todo(todo_id, todo)

    def delete_todo(self, todo_id: int):
        self.todo_repo.delete_todo(todo_id)
        return {"detail": "Todo deleted"}
