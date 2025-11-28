from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env FIRST before importing settings
env_file = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_file)

from app.core.config import settings

# ONLY Azure SQL - No SQLite fallback!
if not settings.DATABASE_URL:
    print("❌ FATAL ERROR: Azure SQL credentials not configured!")
    print("   Set these in .env file or environment variables:")
    print("   - AZURE_SQL_SERVER")
    print("   - AZURE_SQL_DATABASE")
    print("   - AZURE_SQL_USERNAME")
    print("   - AZURE_SQL_PASSWORD")
    raise RuntimeError("Database credentials not configured")

print(f"✅ Using AZURE SQL: {settings.AZURE_SQL_SERVER}")
database_url = settings.DATABASE_URL
engine_kwargs = {"echo": False}

engine = create_engine(database_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
