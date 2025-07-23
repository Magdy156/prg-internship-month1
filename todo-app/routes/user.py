from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserResponse
from db.database import session
from routes.auth import get_password_hash, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    db_user_check = db.query(User).filter(User.username == user.username).first()
    if db_user_check and db_user_check.id != user_id:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_check = db.query(User).filter(User.email == user.email).first()
    if db_user_check and db_user_check.id != user_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}
