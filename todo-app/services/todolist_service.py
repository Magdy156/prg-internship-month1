from fastapi import Depends
from schemas.todolist import TodoListCreate, TodoListResponse
from dal.repositories.todolist_repository import TodoListRepository
from utils.dependencies import get_todolist_repository

class TodoListService:
    def __init__(self, todo_repo: TodoListRepository = Depends(get_todolist_repository)):
        self.todo_repo = todo_repo

    def create_todo(self, todo: TodoListCreate, user_id: int) -> TodoListResponse:
        return self.todo_repo.create_todo(todo, user_id)

    def get_todo(self, todo_id: int) -> TodoListResponse:
        return self.todo_repo.get_todo(todo_id)

    def update_todo(self, todo_id: int, todo: TodoListCreate) -> TodoListResponse:
        return self.todo_repo.update_todo(todo_id, todo)

    def delete_todo(self, todo_id: int):
        self.todo_repo.delete_todo(todo_id)
