# Resource Management Dashboard

## Overview
Full-stack application for resource management with:
- **Frontend**: React + Vite + TypeScript (port 5000)
- **Backend**: FastAPI + SQLAlchemy (port 8000)  
- **Database**: SQLite (development, auto-initialized)

## Project Structure
```
├── frontend/              # React/Vite app (port 5000)
│   ├── src/
│   ├── package.json
│   └── vite.config.ts    # Already configured for Replit
├── backend/              # FastAPI app (port 8000)
│   ├── app/
│   ├── run.py
│   ├── requirements.txt
│   └── .env             # Configuration file
└── database/            # SQL schemas
```

## Setup Complete ✓
- Frontend: npm install complete, running on port 5000
- Backend: uvicorn + FastAPI configured, running on port 8000
- Database: SQLite auto-creates tables on startup
- Deployment: VM configuration set up for production
- CORS: Enabled for frontend-backend communication

## Key Features
- User authentication with JWT
- Admin panel for user management
- Resource management system
- Theme switching
- CORS properly configured

## Login Credentials (Default Super User)
- Email: admin@example.com
- Password: admin123

## Running
- Frontend automatically runs on port 5000 (managed by workflow)
- Backend runs on port 8000 (background process)
- Both configured to communicate automatically
