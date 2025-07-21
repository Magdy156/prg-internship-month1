from fastapi import FastAPI
import uvicorn
from sqlalchemy import text
from db.database import engine


app = FastAPI()

@app.get('/')
def root():
    return {"Message": "Hello World!!"}

# Test connection on startup
@app.on_event("startup")
def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("Database connected successfully!")
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
