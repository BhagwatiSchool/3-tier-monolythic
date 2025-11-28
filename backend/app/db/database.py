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

# Determine database to use
database_url = None
engine_kwargs = {}

# Try Azure SQL first if credentials are configured
if settings.DATABASE_URL:
    try:
        # Test connection to Azure SQL
        test_engine = create_engine(settings.DATABASE_URL, **{"echo": False, "pool_pre_ping": True})
        test_engine.connect().close()
        database_url = settings.DATABASE_URL
        engine_kwargs = {"echo": False}
        print(f"✅ Using AZURE SQL: {settings.AZURE_SQL_SERVER}")
    except Exception as e:
        print(f"⚠️  Azure SQL unavailable: {str(e)[:50]}...")
        database_url = None

# Fallback to SQLite if Azure not available
if not database_url:
    print("Using SQLite (local development/Replit)")
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
