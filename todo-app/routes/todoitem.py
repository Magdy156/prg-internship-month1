from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.todoitem import TodoItem
from models.todo import Todo
from schemas.todoitem import TodoItemCreate, TodoItemResponse
from db.database import session
from routes.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/todoitems", tags=["todoitems"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TodoItemResponse)
def create_todo_item(todo_item: TodoItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_item.todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add items to this todo")
    db_todo_item = TodoItem(**todo_item.dict())
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@router.get("/{todo_item_id}", response_model=TodoItemResponse)
def read_todo_item(todo_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db_todo = db.query(Todo).filter(Todo.id == todo_item.todo_id).first()
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo item")
    return todo_item

@router.put("/{todo_item_id}", response_model=TodoItemResponse)
def update_todo_item(todo_item_id: int, todo_item: TodoItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db_todo = db.query(Todo).filter(Todo.id == todo_item.todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo item")
    for key, value in todo_item.dict().items():
        setattr(db_todo_item, key, value)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@router.delete("/{todo_item_id}")
def delete_todo_item(todo_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db_todo = db.query(Todo).filter(Todo.id == db_todo_item.todo_id).first()
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo item")
    db.delete(db_todo_item)
    db.commit()
    return {"detail": "TodoItem deleted"}
