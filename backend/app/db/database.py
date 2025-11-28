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

# Use Azure SQL if credentials available, else fallback to SQLite
if settings.DATABASE_URL:
    # Azure SQL - using your credentials
    print(f"✅ Using Azure SQL Server: {settings.AZURE_SQL_SERVER}")
    print(f"✅ Database: {settings.AZURE_SQL_DATABASE}")
    database_url = settings.DATABASE_URL
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
        "echo": False
    }
else:
    # Fallback to SQLite if no credentials
    print("⚠️  Using SQLite (no Azure SQL credentials configured)")
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
