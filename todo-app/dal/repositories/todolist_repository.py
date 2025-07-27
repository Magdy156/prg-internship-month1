from sqlalchemy.orm import Session
from models.todolist import TodoList
from schemas.todolist import TodoListCreate, TodoListUpdate, TodoListResponse
from utils.exceptions import TodoListNotFoundException
from datetime import datetime, timezone

class TodoListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo(self, todolist: TodoListCreate, user_id: int) -> TodoListResponse:
        data = todolist.model_dump()
        data['user_id'] = user_id
        data['created_at'] = datetime.now(timezone.utc)
        data['updated_at'] = datetime.now(timezone.utc)
        db_todolist = TodoList(**data)
        self.db.add(db_todolist)
        self.db.commit()
        self.db.refresh(db_todolist)
        return TodoListResponse.model_validate(db_todolist)

    def get_todo(self, todo_id: int) -> TodoListResponse:
        todo = self.db.query(TodoList).filter(TodoList.id == todo_id).first()
        if todo is None:
            raise TodoListNotFoundException()
        return TodoListResponse.model_validate(todo)

    def update_todo(self, todo_id: int, todolist: TodoListUpdate) -> TodoListResponse:
        db_todolist = self.db.query(TodoList).filter(TodoList.id == todo_id).first()
        if db_todolist is None:
            raise TodoListNotFoundException()
        update_data = todolist.model_dump(exclude_unset=True)
        update_data['updated_at'] = datetime.now(timezone.utc)
        self.db.query(TodoList).filter(TodoList.id == todo_id).update(update_data)
        self.db.commit()
        self.db.refresh(db_todolist)
        return TodoListResponse.model_validate(db_todolist)

    def delete_todo(self, todo_id: int):
        db_todolist = self.db.query(TodoList).filter(TodoList.id == todo_id).first()
        if db_todolist is None:
            raise TodoListNotFoundException()
        self.db.delete(db_todolist)
        self.db.commit()
