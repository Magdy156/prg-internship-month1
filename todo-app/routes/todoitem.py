from fastapi import APIRouter, Depends, status
from schemas.todoitem import TodoItemCreate, TodoItemResponse
from services.todoitem_service import TodoItemService
from models.user import User
from utils.auth_utils import get_current_user
from utils.dependencies import get_todoitem_service

router = APIRouter(prefix="/todoitems", tags=["todoitems"])

@router.post("/", response_model=TodoItemResponse)
def create_todo_item(todo_item: TodoItemCreate, current_user: User = Depends(get_current_user), todoitem_service: TodoItemService = Depends(get_todoitem_service)):
    return todoitem_service.create_todo_item(todo_item, todo_item.todolist_id)

@router.get("/{todo_item_id}", response_model=TodoItemResponse)
def read_todo_item(todo_item_id: int, current_user: User = Depends(get_current_user), todoitem_service: TodoItemService = Depends(get_todoitem_service)):
    return todoitem_service.get_todo_item(todo_item_id)

@router.put("/{todo_item_id}", response_model=TodoItemResponse)
def update_todo_item(todo_item_id: int, todo_item: TodoItemCreate, current_user: User = Depends(get_current_user), todoitem_service: TodoItemService = Depends(get_todoitem_service)):
    return todoitem_service.update_todo_item(todo_item_id, todo_item)

@router.delete("/{todo_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_item(todo_item_id: int, current_user: User = Depends(get_current_user), todoitem_service: TodoItemService = Depends(get_todoitem_service)):
    todoitem_service.delete_todo_item(todo_item_id)
    return None
