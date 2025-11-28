#!/usr/bin/env python3
"""
Automatically create Azure SQL schema using credentials from .env
Usage: python create_azure_schema.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from home directory
env_path = Path.home() / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded .env from: {env_path}")
else:
    print(f"❌ .env not found at: {env_path}")
    sys.exit(1)

# Get credentials
server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USERNAME")
password = os.getenv("AZURE_SQL_PASSWORD")

if not all([server, database, username, password]):
    print("❌ Missing credentials in .env file!")
    print(f"   SERVER: {server}")
    print(f"   DATABASE: {database}")
    print(f"   USERNAME: {username}")
    print(f"   PASSWORD: {'*' * len(password) if password else 'NOT SET'}")
    sys.exit(1)

print(f"✅ Credentials found:")
print(f"   Server: {server}")
print(f"   Database: {database}")
print(f"   Username: {username}")

# Import pymssql
try:
    import pymssql
except ImportError:
    print("❌ pymssql not installed. Run: pip install pymssql")
    sys.exit(1)

# Connect to Azure SQL
try:
    print("\n🔄 Connecting to Azure SQL...")
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    print("✅ Connected to Azure SQL!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# SQL Scripts to create schema
schema_scripts = [
    # 1. Create Users Table
    """
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
    BEGIN
        CREATE TABLE users (
            id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
            email NVARCHAR(255) NOT NULL UNIQUE,
            hashed_password NVARCHAR(255) NOT NULL,
            display_name NVARCHAR(100),
            tagline NVARCHAR(200),
            bio NVARCHAR(500),
            avatar_url NVARCHAR(500),
            role NVARCHAR(20) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
            is_protected BIT NOT NULL DEFAULT 0,
            created_at DATETIME2 DEFAULT GETDATE(),
            INDEX IX_users_email (email)
        );
        PRINT 'Created users table';
    END
    ELSE
    BEGIN
        PRINT 'Users table already exists';
    END;
    """,
    
    # 2. Add Missing Columns to Users
    """
    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' AND COLUMN_NAME='tagline')
        ALTER TABLE users ADD tagline NVARCHAR(200) NULL;
    
    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' AND COLUMN_NAME='is_protected')
        ALTER TABLE users ADD is_protected BIT NOT NULL DEFAULT 0;
    
    PRINT 'Verified all columns in users table';
    """,
    
    # 3. Create Theme Config Table
    """
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'theme_config')
    BEGIN
        CREATE TABLE theme_config (
            id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
            config_key NVARCHAR(100) NOT NULL UNIQUE,
            config_value NVARCHAR(500) NOT NULL,
            created_at DATETIME2 DEFAULT GETDATE(),
            updated_at DATETIME2 DEFAULT GETDATE()
        );
        PRINT 'Created theme_config table';
    END
    ELSE
    BEGIN
        PRINT 'Theme config table already exists';
    END;
    """,
    
    # 4. Insert Default Theme Configuration
    """
    IF NOT EXISTS (SELECT * FROM theme_config WHERE config_key = 'primary_color')
    BEGIN
        INSERT INTO theme_config (config_key, config_value) VALUES
        ('primary_color', '222.2 47.4% 11.2%'),
        ('primary_foreground', '210 40% 98%'),
        ('secondary_color', '210 40% 96.1%'),
        ('secondary_foreground', '222.2 47.4% 11.2%'),
        ('accent_color', '210 40% 96.1%'),
        ('accent_foreground', '222.2 47.4% 11.2%'),
        ('background_color', '0 0% 100%'),
        ('foreground_color', '222.2 84% 4.9%');
        PRINT 'Inserted default theme configuration';
    END
    ELSE
    BEGIN
        PRINT 'Theme configuration already exists';
    END;
    """
]

# Execute schema creation scripts
print("\n🔄 Creating schema...\n")
for i, script in enumerate(schema_scripts, 1):
    try:
        print(f"   Executing script {i}/4...")
        cursor.execute(script)
        conn.commit()
        print(f"   ✅ Script {i} completed")
    except Exception as e:
        print(f"   ⚠️  Script {i}: {e}")
        conn.rollback()

# Verify schema
print("\n🔍 Verifying schema...\n")
try:
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    tables = cursor.fetchall()
    print("✅ Tables in database:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Check users table columns
    print("\n✅ Columns in 'users' table:")
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'users'
        ORDER BY ORDINAL_POSITION
    """)
    columns = cursor.fetchall()
    for col_name, data_type, is_nullable in columns:
        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
        print(f"   - {col_name}: {data_type} {nullable}")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")

# Close connection
cursor.close()
conn.close()

print("\n✅ Schema creation completed!")
print("\n🚀 Next: Restart your backend")
print("   cd ~/app")
print("   pkill -f uvicorn")
print("   uvicorn app.main:app --host 0.0.0.0 --port 8000")
