# Resource Management Dashboard - Ready to Use ✅

## Status: Working! 🎉
Your full-stack app is fully set up and running in Replit.

## Architecture
```
Frontend (React/Vite/TypeScript) → Port 5000
     ↓ (proxy via /api)
Backend (FastAPI) → Port 8000
     ↓
Database (SQLite - auto-initialized)
```

## How to Use

1. **Frontend automatically runs** on port 5000 (via workflow)
2. **Start backend** manually with:
   ```bash
   cd backend && python run.py
   ```
3. **Login with default admin:**
   - Email: `admin@example.com`
   - Password: `admin123`

## Features
- ✅ User authentication (JWT tokens)
- ✅ Admin user management panel
- ✅ Resource management system
- ✅ Theme switching (light/dark)
- ✅ User profiles with avatars
- ✅ CORS enabled for frontend-backend communication

## File Structure
```
backend/
  ├── app/
  │   ├── api/          # API routes (auth, users, resources, etc)
  │   ├── models/       # Database models
  │   ├── schemas/      # Pydantic schemas
  │   ├── core/         # Config, security
  │   ├── db/           # Database setup
  │   └── main.py       # FastAPI app setup
  ├── run.py           # Start command
  └── .env             # Environment config
  
frontend/
  ├── src/
  │   ├── pages/       # Auth, Dashboard, Settings, etc
  │   ├── components/  # UI components
  │   ├── lib/         # API client, utilities
  │   └── types/       # TypeScript types
  ├── vite.config.ts   # Vite config (proxy to backend)
  └── package.json
```

## Database
- **Type:** SQLite (local development)
- **Auto-init:** Tables created on first backend startup
- **Location:** `backend/data/app.db`
- **Super user:** Pre-created at startup (admin@example.com / admin123)

## Deployment
Configured for VM deployment. Build and run commands:
- **Build:** `cd frontend && npm run build`
- **Run:** `cd backend && python run.py & cd frontend && npm run dev`

## Troubleshooting
- If login fails: Restart backend (`cd backend && python run.py`)
- If frontend shows blank: Clear browser cache and refresh
- If API calls fail: Ensure backend is running on port 8000
