from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from dal.repositories.todolist_repository import TodoListRepository
from schemas.todolist import TodoListCreate, TodoListResponse
from models.todolist import TodoList
from db.database import get_db

class TodoListService:
    def __init__(self, db: Session = Depends(get_db)):
        self.todo_repo = TodoListRepository(db)

    def create_todo(self, todo: TodoListCreate, user_id: int) -> TodoList:
        return self.todo_repo.create_todo(todo, user_id)

    def get_todo(self, todo_id: int) -> TodoList:
        return self.todo_repo.get_todo(todo_id)

    def update_todo(self, todo_id: int, todo: TodoListCreate) -> TodoList:
        return self.todo_repo.update_todo(todo_id, todo)

    def delete_todo(self, todo_id: int):
        if not self.todo_repo.get_todo(todo_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TodoList not found")
        self.todo_repo.delete_todo(todo_id)
