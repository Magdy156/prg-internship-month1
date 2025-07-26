from sqlalchemy.orm import Session
from models.todoitem import TodoItem
from schemas.todoitem import TodoItemCreate
from fastapi import HTTPException, status

class TodoItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo_item(self, todo_item: TodoItemCreate, todolist_id: int) -> TodoItem:
        db_todo_item = TodoItem(
            title=todo_item.title,
            description=todo_item.description,
            completed=todo_item.completed,
            created_at=todo_item.created_at if hasattr(todo_item, 'created_at') else None,
            updated_at=todo_item.updated_at if hasattr(todo_item, 'updated_at') else None,
            due_date=todo_item.due_date,
            priority=todo_item.priority.value if todo_item.priority else None,
            category=todo_item.category,
            todolist_id=todolist_id
        )
        self.db.add(db_todo_item)
        self.db.commit()
        self.db.refresh(db_todo_item)
        return db_todo_item

    def get_todo_item(self, todo_item_id: int) -> TodoItem:
        todo_item = self.db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
        if todo_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TodoItem not found")
        return todo_item

    def update_todo_item(self, todo_item_id: int, todo_item: TodoItemCreate) -> TodoItem:
        db_todo_item = self.get_todo_item(todo_item_id)
        db_todo_item.title = todo_item.title
        db_todo_item.description = todo_item.description
        db_todo_item.completed = todo_item.completed
        db_todo_item.due_date = todo_item.due_date
        db_todo_item.priority = todo_item.priority.value if todo_item.priority else None
        db_todo_item.category = todo_item.category
        self.db.commit()
        self.db.refresh(db_todo_item)
        return db_todo_item

    def delete_todo_item(self, todo_item_id: int):
        db_todo_item = self.get_todo_item(todo_item_id)
        self.db.delete(db_todo_item)
        self.db.commit()
