# dal/repositories/todoitem_repository.py
from sqlalchemy.orm import Session
from models.todoitem import TodoItem
from models.todolist import TodoList
from schemas.todoitem import TodoItemCreate, TodoItemUpdate, TodoItemResponse
from utils.exceptions import TodoItemNotFoundException, TodoListNotFoundException
from datetime import datetime, timezone

class TodoItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_todo_item(self, todo_item: TodoItemCreate, todolist_id: int) -> TodoItemResponse:
        todolist = self.db.query(TodoList).filter(TodoList.id == todolist_id).first()
        if not todolist:
            raise TodoListNotFoundException()
        data = todo_item.model_dump()
        data['priority'] = data['priority'].value if data['priority'] else None
        data['todolist_id'] = todolist_id
        data['created_at'] = datetime.now(timezone.utc)
        data['updated_at'] = datetime.now(timezone.utc)
        db_todo_item = TodoItem(**data)
        self.db.add(db_todo_item)
        self.db.commit()
        self.db.refresh(db_todo_item)
        return TodoItemResponse.model_validate(db_todo_item)

    def get_todo_item(self, todo_item_id: int) -> TodoItemResponse:
        todo_item = self.db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
        if todo_item is None:
            raise TodoItemNotFoundException()
        return TodoItemResponse.model_validate(todo_item)

    def update_todo_item(self, todo_item_id: int, todo_item: TodoItemUpdate) -> TodoItemResponse:
        db_todo_item = self.db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
        if db_todo_item is None:
            raise TodoItemNotFoundException()
        update_data = todo_item.model_dump(exclude_unset=True)
        if 'priority' in update_data:
            update_data['priority'] = update_data['priority'].value if update_data['priority'] else None
        update_data['updated_at'] = datetime.now(timezone.utc)
        self.db.query(TodoItem).filter(TodoItem.id == todo_item_id).update(update_data)
        self.db.commit()
        self.db.refresh(db_todo_item)
        return TodoItemResponse.model_validate(db_todo_item)

    def delete_todo_item(self, todo_item_id: int):
        db_todo_item = self.db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
        if db_todo_item is None:
            raise TodoItemNotFoundException()
        self.db.delete(db_todo_item)
        self.db.commit()
