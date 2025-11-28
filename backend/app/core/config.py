import os
from urllib.parse import quote
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from multiple possible locations
# Try: current dir, backend dir, and parent dir
possible_paths = [
    Path.cwd() / '.env',  # Current working directory
    Path(__file__).resolve().parent.parent.parent / '.env',  # Relative to this file
    Path('/home/azureuser/app/.env'),  # VM default location
    Path('/home/azureuser/.env'),  # VM home
]

for env_path in possible_paths:
    if env_path.exists():
        print(f"✅ Loading .env from: {env_path}")
        load_dotenv(dotenv_path=env_path, override=True)
        break
else:
    print("⚠️  No .env file found - using environment variables")

class Settings:
    """Settings class that reads from environment variables"""
    
    def __init__(self):
        # Database Configuration - ALWAYS read from credentials
        self.AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "")
        self.AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "")
        self.AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME", "")
        self.AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "")
        
        # Security Configuration
        self.SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key-change-in-production")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        
        # CORS Configuration
        self.CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
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
    
    @property
    def cors_allowed_origins(self) -> list:
        """Parse CORS_ALLOW_ORIGINS into a list for FastAPI middleware"""
        if self.CORS_ALLOW_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ALLOW_ORIGINS.split(",") if origin.strip()]


settings = Settings()
if settings.AZURE_SQL_SERVER:
    print(f"✅ Server configured for: {settings.AZURE_SQL_SERVER}")
else:
    print("⚠️  Database credentials not configured. Set environment variables.")
