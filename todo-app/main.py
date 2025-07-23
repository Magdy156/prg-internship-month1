from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import text
from db.database import engine, Base
from routes import user_router, todo_router, todoitem_router, auth_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() != 1:
                raise HTTPException(status_code=500, detail="Database connection test failed")
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Database connected successfully!")
        print("Tables (users, todos, todoitems) created if not exist.")
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    yield
    print("Application shutting down")

app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)
app.include_router(todoitem_router)

@app.get('/')
def root():
    print("Received request at /")
    return {"Message": "Hello World!!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
