from fastapi import APIRouter, Depends, HTTPException, status
from schemas.todo import TodoCreate, TodoResponse
from services.todo_service import TodoService
from models.user import User
from routes.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user), todo_service: TodoService = Depends()):
    return todo_service.create_todo(todo, current_user.id)

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, current_user: User = Depends(get_current_user), todo_service: TodoService = Depends()):
    return todo_service.get_todo(todo_id)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, current_user: User = Depends(get_current_user), todo_service: TodoService = Depends()):
    return todo_service.update_todo(todo_id, todo)

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), todo_service: TodoService = Depends()):
    return todo_service.delete_todo(todo_id)
