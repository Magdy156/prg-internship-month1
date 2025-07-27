from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db
from dal.repositories.user_repository import UserRepository
from dal.repositories.todolist_repository import TodoListRepository
from dal.repositories.todoitem_repository import TodoItemRepository

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_todolist_repository(db: Session = Depends(get_db)):
    return TodoListRepository(db)

def get_todoitem_repository(db: Session = Depends(get_db)):
    return TodoItemRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    from services.user_service import UserService  # Lazy import
    return UserService(user_repository)

def get_todolist_service(todolist_repository: TodoListRepository = Depends(get_todolist_repository)):
    from services.todolist_service import TodoListService  # Lazy import
    return TodoListService(todolist_repository)

def get_todoitem_service(todoitem_repository: TodoItemRepository = Depends(get_todoitem_repository)):
    from services.todoitem_service import TodoItemService  # Lazy import
    return TodoItemService(todoitem_repository)
