from sqlalchemy.orm import Session
from models.todoitem import TodoItem
from schemas.todoitem import TodoItemCreate
from fastapi import HTTPException, status

class TodoItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo_item(self, todo_item: TodoItemCreate, todolist_id: int) -> TodoItem:
        data = todo_item.model_dump()
        data['priority'] = data['priority'].value if data['priority'] else None
        data['todolist_id'] = todolist_id
        db_todo_item = TodoItem(**data)
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
        update_data = todo_item.model_dump(exclude_unset=True)
        if 'priority' in update_data:
            update_data['priority'] = update_data['priority'].value if update_data['priority'] else None
        for key, value in update_data.items():
            setattr(db_todo_item, key, value)
        self.db.commit()
        self.db.refresh(db_todo_item)
        return db_todo_item

    def delete_todo_item(self, todo_item_id: int):
        db_todo_item = self.get_todo_item(todo_item_id)
        self.db.delete(db_todo_item)
        self.db.commit()
