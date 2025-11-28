from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env FIRST before importing settings
env_file = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_file)

from app.core.config import settings

# Determine database connection
if settings.AZURE_SQL_SERVER and settings.AZURE_SQL_DATABASE:
    print(f"✅ Using Azure SQL: {settings.AZURE_SQL_SERVER}")
    database_url = settings.DATABASE_URL
    engine_kwargs = {"echo": False}
else:
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


def init_db():
    """Initialize database and fix schema if needed"""
    try:
        if "mssql" in str(database_url):
            with engine.begin() as conn:
                # Check if resources table exists and has correct schema
                check_table = text("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'resources'
                """)
                result = conn.execute(check_table)
                table_exists = result.scalar() > 0
                
                need_recreate = False
                if table_exists:
                    # Check user_id type
                    check_type = text("""
                    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'resources' AND COLUMN_NAME = 'user_id'
                    """)
                    result = conn.execute(check_type)
                    data_type = result.scalar()
                    if data_type not in ('varchar', 'nvarchar'):
                        # user_id is wrong type, need to drop and recreate
                        need_recreate = True
                
                if need_recreate:
                    # Drop existing table with wrong schema
                    conn.execute(text("DROP TABLE IF EXISTS resources"))
                    print("✅ Dropped resources table (wrong schema)")
                    table_exists = False
                
                if not table_exists:
                    # Create table with correct schema (without FK to avoid type mismatch)
                    create_table = text("""
                    CREATE TABLE resources (
                        id INT PRIMARY KEY IDENTITY(1,1),
                        user_id VARCHAR(36) NOT NULL,
                        icon VARCHAR(20) NOT NULL,
                        title VARCHAR(100) NOT NULL,
                        resource_name VARCHAR(200) NOT NULL,
                        description VARCHAR(500),
                        status VARCHAR(20) DEFAULT 'Running',
                        region VARCHAR(50) DEFAULT 'East US',
                        created_at DATETIME DEFAULT GETUTCDATE(),
                        updated_at DATETIME DEFAULT GETUTCDATE()
                    );
                    CREATE INDEX idx_resources_user_id ON resources(user_id);
                    """)
                    conn.execute(create_table)
                    print("✅ Created resources table with correct schema")
    except Exception as e:
        print(f"⚠️  Database init error: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
