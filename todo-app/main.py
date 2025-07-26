from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from db.database import engine, Base
from routes import auth_router, user_router, todolist_router, todoitem_router
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
