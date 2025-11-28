from sqlalchemy import create_engine, text, inspect
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


def ensure_columns_exist():
    """Ensure all required columns exist in the users table with correct schema"""
    inspector = inspect(engine)
    
    # Check if users table exists
    if 'users' not in inspector.get_table_names():
        print("ℹ️  Users table doesn't exist yet - will be created by SQLAlchemy")
        return
    
    with engine.connect() as conn:
        # Check if id column is correct type (should be VARCHAR for UUID, not IDENTITY)
        try:
            result = conn.execute(text("""
                SELECT COLUMN_NAME, DATA_TYPE, COLUMNPROPERTY(OBJECT_ID('users'), COLUMN_NAME, 'IsIdentity') as is_identity
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'id'
            """))
            id_info = result.fetchone()
            
            if id_info and id_info[2] == 1:  # is_identity = 1
                # Need to recreate table - it has IDENTITY but we need UUID
                print("⚠️  Recreating users table with correct UUID schema...")
                try:
                    conn.execute(text("DROP TABLE IF EXISTS users"))
                    conn.commit()
                    print("✅ Dropped old users table")
                except:
                    conn.rollback()
        except:
            pass
    
    # Get existing columns in users table
    existing_columns = {col['name'] for col in inspector.get_columns('users')}
    
    # Define required columns
    required_columns = {
        'display_name': 'NVARCHAR(100)',
        'tagline': 'NVARCHAR(200)',
        'bio': 'NVARCHAR(500)',
        'avatar_url': 'NVARCHAR(500)',
        'is_protected': 'BIT DEFAULT 0',
    }
    
    # Add missing columns
    with engine.connect() as conn:
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                try:
                    alter_sql = f"ALTER TABLE users ADD {col_name} {col_type}"
                    conn.execute(text(alter_sql))
                    conn.commit()
                    print(f"✅ Added missing column: {col_name}")
                except Exception as e:
                    print(f"⚠️  Could not add {col_name}: {e}")
                    conn.rollback()
