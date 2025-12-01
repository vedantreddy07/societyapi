from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL - modify for your environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "DATABASE_URL=postgresql://society_management_drv7_user:5i3uNlp76n9hpkyHgjLnfAFYgLVzq47I@dpg-d4mlb9khg0os73bu74jg-a.singapore-postgres.render.com/society_management_drv7"
)

print(f"Connecting to database: {DATABASE_URL.split('@')[1]}")  # Print only host/db, not password

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()