-- Migration: Add missing columns to existing users table
-- Run this if you already have data in the users table

-- Add tagline column if it doesn't exist
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME='users' AND COLUMN_NAME='tagline'
)
BEGIN
    ALTER TABLE users ADD tagline NVARCHAR(200) NULL;
    PRINT 'Added tagline column to users table';
END
ELSE
BEGIN
    PRINT 'tagline column already exists';
END;

-- Add is_protected column if it doesn't exist
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME='users' AND COLUMN_NAME='is_protected'
)
BEGIN
    ALTER TABLE users ADD is_protected BIT NOT NULL DEFAULT 0;
    PRINT 'Added is_protected column to users table';
END
ELSE
BEGIN
    PRINT 'is_protected column already exists';
END;

-- Verify the columns exist
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'users'
ORDER BY ORDINAL_POSITION;
