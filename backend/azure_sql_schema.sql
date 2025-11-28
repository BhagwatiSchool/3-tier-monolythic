-- Azure SQL Database Schema for Resource Management System
-- Run this on your Azure SQL Database

-- Create Users Table
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

-- Create Theme Configuration Table
CREATE TABLE theme_config (
    id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    config_key NVARCHAR(100) NOT NULL UNIQUE,
    config_value NVARCHAR(500) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);

-- Insert Default Theme Configuration
INSERT INTO theme_config (config_key, config_value) VALUES
('primary_color', '222.2 47.4% 11.2%'),
('primary_foreground', '210 40% 98%'),
('secondary_color', '210 40% 96.1%'),
('secondary_foreground', '222.2 47.4% 11.2%'),
('accent_color', '210 40% 96.1%'),
('accent_foreground', '222.2 47.4% 11.2%'),
('background_color', '0 0% 100%'),
('foreground_color', '222.2 84% 4.9%');

-- Create trigger to update updated_at timestamp
GO
CREATE TRIGGER trg_theme_config_updated_at
ON theme_config
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE theme_config
    SET updated_at = GETDATE()
    FROM theme_config tc
    INNER JOIN inserted i ON tc.id = i.id;
END;
GO
