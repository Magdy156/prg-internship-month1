from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import text
from db.database import engine, Base
from routes import auth_router, user_router, todolist_router, todoitem_router
from utils.exceptions import UserNotFoundException, InvalidCredentialsException, JWTDecodeException, UsernameExistsException, TodoListNotFoundException, TodoItemNotFoundException
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting lifespan")
    try:
        with engine.connect() as conn:
            print("Testing database connection")
            result = conn.execute(text("SELECT 1"))
            result_value = result.scalar()
            print(f"Database test result: {result_value}")
            if result_value != 1:
                raise Exception("Database connection test failed")
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Database connected successfully!")
        print("Tables (users, todos, todoitems) created if not exist.")
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise Exception(f"Database connection failed: {str(e)}")
    yield
    print("Application shutting down")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc: UserNotFoundException):
    print(f"UserNotFoundException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(request, exc: InvalidCredentialsException):
    print(f"InvalidCredentialsException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(JWTDecodeException)
async def jwt_decode_exception_handler(request, exc: JWTDecodeException):
    print(f"JWTDecodeException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(UsernameExistsException)
async def username_exists_exception_handler(request, exc: UsernameExistsException):
    print(f"UsernameExistsException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )

@app.exception_handler(TodoListNotFoundException)
async def todolist_not_found_exception_handler(request, exc: TodoListNotFoundException):
    print(f"TodoListNotFoundException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

@app.exception_handler(TodoItemNotFoundException)
async def todoitem_not_found_exception_handler(request, exc: TodoItemNotFoundException):
    print(f"TodoItemNotFoundException: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todolist_router)
app.include_router(todoitem_router)

@app.get('/')
def root():
    print("Received request at /")
    return {"Message": "Hello World!!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
