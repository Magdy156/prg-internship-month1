from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv("DATABASE_URL")
print("Loaded DATABASE_URL:", db_url) # for debugging


engine = create_engine(db_url)


session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
