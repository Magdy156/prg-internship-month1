from fastapi import APIRouter, Depends, HTTPException, status
from schemas.todolist import TodoListCreate, TodoListResponse
from services.todolist_service import TodoListService
from models.user import User
from routes.auth import get_current_user

router = APIRouter(prefix="/todolists", tags=["todolists"])

@router.post("/", response_model=TodoListResponse)
def create_todo(todo: TodoListCreate, current_user: User = Depends(get_current_user), todo_service: TodoListService = Depends()):
    return todo_service.create_todo(todo, current_user.id)

@router.get("/{todolist_id}", response_model=TodoListResponse)
def read_todo(todolist_id: int, current_user: User = Depends(get_current_user), todo_service: TodoListService = Depends()):
    return todo_service.get_todo(todolist_id)

@router.put("/{todolist_id}", response_model=TodoListResponse)
def update_todo(todolist_id: int, todo: TodoListCreate, current_user: User = Depends(get_current_user), todo_service: TodoListService = Depends()):
    return todo_service.update_todo(todolist_id, todo)

@router.delete("/{todolist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todolist_id: int, current_user: User = Depends(get_current_user), todo_service: TodoListService = Depends()):
    todo_service.delete_todo(todolist_id)
    return None
