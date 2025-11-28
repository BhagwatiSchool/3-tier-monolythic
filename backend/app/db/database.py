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

# ONLY use Azure SQL - No SQLite fallback!
if not settings.DATABASE_URL:
    raise RuntimeError(
        "❌ FATAL: Azure SQL credentials not configured!\n\n"
        "Set these environment variables:\n"
        "  AZURE_SQL_SERVER=your-server.database.windows.net\n"
        "  AZURE_SQL_DATABASE=your-database-name\n"
        "  AZURE_SQL_USERNAME=your-admin-username\n"
        "  AZURE_SQL_PASSWORD=your-secure-password"
    )

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
