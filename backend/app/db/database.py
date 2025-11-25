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

# Determine database URL
if settings.DATABASE_URL:
    # Azure SQL connection using pymssql driver
    print(f"🔗 Connecting to: {settings.AZURE_SQL_SERVER}")
    print(f"📊 Database: {settings.AZURE_SQL_DATABASE}")
    print(f"👤 Username: {settings.AZURE_SQL_USERNAME}")
    database_url = settings.DATABASE_URL
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "echo": False
    }
else:
    # Use SQLite for local development
    print("⚠️  Using SQLite for local development")
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
