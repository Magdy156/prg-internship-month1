from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import text
from db.database import engine, Base
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

@app.get('/')
def root():
    return {"Message": "Hello World!!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
