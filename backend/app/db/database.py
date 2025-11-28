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

# Auto-detect environment: Replit uses SQLite, VMs use Azure SQL
is_replit = os.getenv("REPL_ID") is not None

# On Replit: Always use SQLite (Azure SQL firewall blocks Replit)
# On VMs: Use Azure SQL if credentials available, else SQLite
if is_replit or not settings.DATABASE_URL:
    # SQLite for Replit or if no credentials
    print("⚠️  Using SQLite (Replit environment or no Azure credentials)")
    db_dir = Path(__file__).parent.parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    database_url = f"sqlite:///{db_dir}/app.db"
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
        "echo": False
    }
else:
    # Azure SQL for VM deployments
    print(f"✅ Using Azure SQL: {settings.AZURE_SQL_SERVER}")
    database_url = settings.DATABASE_URL
    engine_kwargs = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "connect_args": {"timeout": 10},
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
