#!/bin/bash
# Backend VM Deployment Script
# Run this on Backend VM (4.210.68.49)

set -e

echo "🚀 Deploying Backend to $(hostname -I)"

# 1. Setup Python environment
echo "🐍 Setting up Python environment..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# 2. Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# 3. Setup .env if provided
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using SQLite (default)."
    echo "💡 To use Azure SQL, create .env with:"
    echo "   AZURE_SQL_SERVER=ritserver"
    echo "   AZURE_SQL_USERNAME=your_username"
    echo "   AZURE_SQL_PASSWORD=your_password"
    echo "   AZURE_SQL_DATABASE=resource_management"
fi

# 4. Run backend
echo "🏃 Starting backend on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

echo "✅ Backend running!"
