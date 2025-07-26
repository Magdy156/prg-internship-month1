from sqlalchemy.orm import Session
from models.todolist import TodoList
from schemas.todolist import TodoListCreate
from fastapi import HTTPException, status

class TodoListRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo(self, todolist: TodoListCreate, user_id: int) -> TodoList:
        data = todolist.model_dump()
        data['user_id'] = user_id
        db_todolist = TodoList(**data)
        self.db.add(db_todolist)
        self.db.commit()
        self.db.refresh(db_todolist)
        return db_todolist

    def get_todo(self, todo_id: int) -> TodoList:
        todo = self.db.query(TodoList).filter(TodoList.id == todo_id).first()
        if todo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    def update_todo(self, todo_id: int, todolist: TodoListCreate) -> TodoList:
        db_todolist = self.get_todo(todo_id)
        update_data = todolist.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todolist, key, value)
        self.db.commit()
        self.db.refresh(db_todolist)
        return db_todolist

    def delete_todo(self, todo_id: int):
        db_todo = self.get_todo(todo_id)
        self.db.delete(db_todo)
        self.db.commit()
