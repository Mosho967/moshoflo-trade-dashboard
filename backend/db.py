import os

# Load from .env only during local dev
if os.getenv("GITHUB_ACTIONS") != "true":
    from dotenv import load_dotenv
    load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Pull from env
DATABASE_URL = os.getenv("DATABASE_URL")

# Error check
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

# Create DB engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
