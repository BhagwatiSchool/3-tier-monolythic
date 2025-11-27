# Resource Management Dashboard

## Overview
Full-stack application for resource management with:
- **Frontend**: React + Vite + TypeScript (port 5000)
- **Backend**: FastAPI + SQLAlchemy (port 8000)
- **Database**: SQLite (development)

## Project Structure
```
├── frontend/           # React/Vite app (port 5000)
├── backend/            # FastAPI app (port 8000)
│   ├── app/
│   ├── run.py
│   └── requirements.txt
└── database/           # SQL schemas
```

## Setup
- Frontend already configured to proxy /api to backend
- Vite HMR configured for Replit environment
- Backend auto-creates tables on startup

## Current Status
- Setting up for Replit environment
