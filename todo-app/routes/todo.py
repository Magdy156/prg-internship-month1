from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.todo import Todo
from models.user import User
from schemas.todo import TodoCreate, TodoResponse
from db.database import session
from routes.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = Todo(**todo.dict(), user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}
