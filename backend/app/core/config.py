import os
from urllib.parse import quote

class Settings:
    """Settings class that reads from environment variables"""
    
    def __init__(self):
        self.AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "")
        self.AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "")
        self.AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME", "")
        self.AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key-change-in-production")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5000")
    
    @property
    def DATABASE_URL(self) -> str:
        if not all([self.AZURE_SQL_SERVER, self.AZURE_SQL_DATABASE, self.AZURE_SQL_USERNAME, self.AZURE_SQL_PASSWORD]):
            return ""
        encoded_password = quote(self.AZURE_SQL_PASSWORD, safe='')
        return (
            f"mssql+pymssql://{self.AZURE_SQL_USERNAME}:{encoded_password}"
            f"@{self.AZURE_SQL_SERVER}:1433/{self.AZURE_SQL_DATABASE}"
        )


settings = Settings()
if settings.AZURE_SQL_SERVER:
    print(f"✅ Server configured for: {settings.AZURE_SQL_SERVER}")
else:
    print("⚠️  Database credentials not configured. Set environment variables.")
