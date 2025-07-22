from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.todoitem import TodoItem
from models.todo import Todo
from schemas import TodoItemCreate, TodoItemResponse
from db.database import session

router = APIRouter(prefix="/todoitems", tags=["todoitems"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TodoItemResponse)
def create_todo_item(todo_item: TodoItemCreate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_item.todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo_item = TodoItem(**todo_item.dict())
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@router.get("/{todo_item_id}", response_model=TodoItemResponse)
def read_todo_item(todo_item_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    return todo_item

@router.put("/{todo_item_id}", response_model=TodoItemResponse)
def update_todo_item(todo_item_id: int, todo_item: TodoItemCreate, db: Session = Depends(get_db)):
    db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db_todo = db.query(Todo).filter(Todo.id == todo_item.todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo_item.dict().items():
        setattr(db_todo_item, key, value)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item

@router.delete("/{todo_item_id}")
def delete_todo_item(todo_item_id: int, db: Session = Depends(get_db)):
    db_todo_item = db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()
    if db_todo_item is None:
        raise HTTPException(status_code=404, detail="TodoItem not found")
    db.delete(db_todo_item)
    db.commit()
    return {"detail": "TodoItem deleted"}
