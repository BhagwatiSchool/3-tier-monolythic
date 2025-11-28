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

# Smart database selection:
# 1. Production VMs: Use Azure SQL (credentials from .env)
# 2. Replit: Fall back to SQLite (for testing only)

if settings.DATABASE_URL:
    database_url = settings.DATABASE_URL
    engine_kwargs = {"echo": False}
    print(f"✅ Using AZURE SQL: {settings.AZURE_SQL_SERVER}")
else:
    # Fallback to SQLite for Replit testing
    print("⚠️  Using SQLite (Replit/Local)")
    db_dir = Path(__file__).parent.parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    database_url = f"sqlite:///{db_dir}/app.db"
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "echo": False
    }

engine = create_engine(database_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
