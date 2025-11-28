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
                # Fix resources table
                check_table = text("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'resources'
                """)
                result = conn.execute(check_table)
                resources_exists = result.scalar() > 0
                
                if resources_exists:
                    check_type = text("""
                    SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'resources' AND COLUMN_NAME = 'user_id'
                    """)
                    result = conn.execute(check_type)
                    data_type = result.scalar()
                    if data_type not in ('varchar', 'nvarchar'):
                        conn.execute(text("DROP TABLE IF EXISTS resources"))
                        resources_exists = False
                
                if not resources_exists:
                    conn.execute(text("""
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
                    """))
                    print("✅ Created resources table")
                
                # Fix theme_config table
                check_theme = text("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'theme_config'
                """)
                result = conn.execute(check_theme)
                theme_exists = result.scalar() > 0
                
                if theme_exists:
                    # Check if it has correct columns
                    check_cols = text("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'theme_config' AND COLUMN_NAME = 'config_key'
                    """)
                    result = conn.execute(check_cols)
                    has_config_key = result.scalar() > 0
                    
                    if not has_config_key:
                        conn.execute(text("DROP TABLE IF EXISTS theme_config"))
                        theme_exists = False
                
                if not theme_exists:
                    conn.execute(text("""
                    CREATE TABLE theme_config (
                        id INT PRIMARY KEY IDENTITY(1,1),
                        config_key VARCHAR(100) UNIQUE NOT NULL,
                        config_value VARCHAR(500) NOT NULL,
                        created_at DATETIME DEFAULT GETUTCDATE(),
                        updated_at DATETIME DEFAULT GETUTCDATE()
                    );
                    CREATE INDEX idx_theme_config_key ON theme_config(config_key);
                    """))
                    print("✅ Created theme_config table")
    except Exception as e:
        print(f"⚠️  Database init error: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
