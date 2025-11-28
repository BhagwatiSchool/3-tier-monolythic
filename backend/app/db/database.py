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

# Always use SQLite for now (Azure SQL connectivity issues need firewall setup)
# TODO: Configure Azure SQL firewall rules to allow Replit IPs
print("⚠️  Using SQLite for development/production")
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
