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


def init_db():
    """Initialize database tables using raw SQL for Azure SQL compatibility"""
    try:
        from sqlalchemy import text
        with engine.begin() as conn:
            # Create resources table if it doesn't exist (Azure SQL compatible)
            create_resources_sql = text("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'resources')
            BEGIN
                CREATE TABLE resources (
                    id INT PRIMARY KEY IDENTITY(1,1),
                    user_id INT NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    resource_name VARCHAR(200) NOT NULL,
                    description VARCHAR(500),
                    status VARCHAR(20) DEFAULT 'Running',
                    region VARCHAR(50) DEFAULT 'East US',
                    created_at DATETIME DEFAULT GETUTCDATE(),
                    updated_at DATETIME DEFAULT GETUTCDATE(),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                CREATE INDEX idx_resources_user_id ON resources(user_id);
            END
            """)
            conn.execute(create_resources_sql)
    except Exception as e:
        print(f"⚠️  Resources table init error (may already exist): {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
