from sqlalchemy.orm import Session
from models.todolist import TodoList
from schemas.todolist import TodoListCreate
from fastapi import HTTPException, status

class TodoListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo(self, todo: TodoListCreate, user_id: int) -> TodoList:
        db_todo = TodoList(
            title=todo.title,
            created_at=todo.created_at if hasattr(todo, 'created_at') else None,
            updated_at=todo.updated_at if hasattr(todo, 'updated_at') else None,
            user_id=user_id
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def get_todo(self, todo_id: int) -> TodoList:
        todo = self.db.query(TodoList).filter(TodoList.id == todo_id).first()
        if todo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    def update_todo(self, todo_id: int, todo: TodoListCreate) -> TodoList:
        db_todo = self.get_todo(todo_id)
        db_todo.title = todo.title
        db_todo.updated_at = todo.updated_at if hasattr(todo, 'updated_at') else None
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def delete_todo(self, todo_id: int):
        db_todo = self.get_todo(todo_id)
        self.db.delete(db_todo)
        self.db.commit()
