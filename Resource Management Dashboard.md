# Resource Management Dashboard

## Overview
A full-stack resource management dashboard application with user authentication, role-based access control, and theme customization. Built with React + Vite on the frontend and Python FastAPI on the backend.

**Status**: Production-ready with full mobile responsiveness
**Last Updated**: November 25, 2025 (Evening)

## Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **UI Components**: Shadcn UI + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router v6

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (local development) / Azure SQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt + passlib

## Project Structure

```
.
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── contexts/     # React contexts (Auth)
│   │   ├── pages/        # Page components
│   │   ├── lib/          # Utilities and API client
│   │   └── types/        # TypeScript type definitions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API route handlers
│   │   ├── core/        # Core configuration
│   │   ├── db/          # Database configuration
│   │   ├── models/      # SQLAlchemy models
│   │   └── schemas/     # Pydantic schemas
│   ├── data/            # SQLite database (gitignored)
│   ├── requirements.txt
│   └── run.py
│
└── database/            # SQL scripts for Azure SQL setup
```

## Key Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin/User)
- Protected admin user that cannot be deleted
- Email + password authentication

### User Management
- User registration and login
- Profile management (display name, tagline, bio, avatar)
- Admin panel for user management
- Role assignment (admin only)

### Resource Management
- Create, read, update, delete resources
- User-specific resource ownership
- Resource metadata (icon, title, name, description, status, region)
- Real-time resource statistics on dashboard

### Theme Customization
- Light/Dark mode
- Pre-defined color schemes
- Persistent theme preferences via backend API
- Dynamic CSS variable updates

### Dashboard
- Resource count statistics
- Visual resource cards
- Admin user management panel
- Profile and settings pages

## Configuration

### Environment Variable Support ⭐ NEW
The backend now supports  **environment variables**:

1. **`.env` File** (VM Deployment)
   - Copy `backend/.env.example` to `backend/.env`
   - Fill in your production values
   - Perfect for Azure VM deployment


**Priority**: `.env` file > Environment Variables > Default values

📖 See `backend/ENV_CONFIG_GUIDE.md` for complete documentation


### Database
- **Development**: Uses SQLite (`backend/data/app.db`)
- **Production**: Can be configured for Azure SQL Database via environment variables

### Default Admin User
A protected admin user is automatically created on first run:
- **Email**: ritesh@apka.bhai
- **Password**: (check backend/app/db/super_user_seed.py for default)
- **Role**: admin
- **Protected**: Cannot be deleted


### Mobile Responsive Design ⭐ NEW
1. **User Management Page Responsive Layout**
   - Flex layout to stack vertically on mobile (< 768px)
   - Added proper breakpoints: `flex-col md:flex-row` for responsive stacking
   - Made dropdown select full-width on mobile, fixed width on desktop
   - Delete button now full-width on mobile for better touch targets
   - Added `min-w-0` and `flex-shrink-0` to prevent text overflow
   - Email text now wraps properly on small screens

2. **Responsive Classes Applied**
   - Main controls: `flex flex-col sm:flex-row` for mobile/tablet/desktop responsiveness
   - Select dropdown: `w-full sm:w-48` for responsive sizing
   - Delete button: `w-full sm:w-auto` for full-width mobile access
   - Icons: `flex-shrink-0` to maintain size on all screens

3. **Result**: 
   - Desktop: Horizontal layout with all controls on one line (✓ Tested)
   - Mobile: Vertical stacking with full-width controls (✓ Fixed)
   - All screens: Proper text wrapping and no overflow

### Production Deployment Configuration ⭐
1. **Dual Environment Variable Support**
   - Added support for both `.env` files and environment variables
   - Created `backend/.env.example` with comprehensive documentation
   - Created `backend/ENV_CONFIG_GUIDE.md` with step-by-step setup guides
   - Priority: `.env` file > Environment Variables > Defaults

2. **Production-Ready Settings**
   - Updated `run.py` to support production mode (0.0.0.0 host, configurable workers)
   - Centralized all configuration in Settings class (`backend/app/core/config.py`)
   - CORS configuration now supports specific origins via `CORS_ALLOW_ORIGINS`
   - Environment-based reload and worker configuration

3. **Configuration Variables**
   - `APP_ENV`: development/production mode switch
   - `PORT`: Configurable server port (default: 8000)
   - `UVICORN_WORKERS`: Number of workers for production
   - `CORS_ALLOW_ORIGINS`: Comma-separated allowed origins
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time


### Code Fixes
- Removed Azure SQL-specific `UNIQUEIDENTIFIER` type from Resource model
- Changed to `String(36)` for UUID compatibility with SQLite
- Removed HMR host restrictions from Vite config
- Centralized CORS and configuration in Settings class

## Deployment

The project is configured for autoscale deployment:
- **Build**: Compiles frontend React app to static assets
- **Run**: Starts both backend API server and frontend preview server
- Frontend serves from `/` with API proxy to backend on `/api`

## Environment Variables

The backend supports configuration via **both `.env` file and environment variables**. See `backend/ENV_CONFIG_GUIDE.md` for complete setup instructions.

### Required for Production (Azure SQL):
- `APP_ENV=production`: Enables production mode
- `PORT=8000`: Server port
- `UVICORN_WORKERS=4`: Number of worker processes
- `AZURE_SQL_SERVER`: Azure SQL server hostname
- `AZURE_SQL_DATABASE`: Database name
- `AZURE_SQL_USERNAME`: Database username
- `AZURE_SQL_PASSWORD`: Database password
- `SECRET_KEY`: JWT secret key (minimum 32 characters)
- `CORS_ALLOW_ORIGINS`: Comma-separated allowed origins
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`: JWT token expiration

### Optional:
- `FRONTEND_URL`: Frontend URL reference (default: http://localhost:5000)
- `LOG_LEVEL`: Logging level (default: INFO)

### Development (SQLite):
Minimal setup required - just `SECRET_KEY` and optionally `CORS_ALLOW_ORIGINS=*`

## User Preferences

No specific user preferences recorded yet. The application follows standard conventions:
- TypeScript for type safety
- Component-based architecture
- RESTful API design
- JWT authentication
- Role-based access control

## Notes

### SQLite vs Azure SQL
The application is designed to work with both SQLite (development) and Azure SQL (production). SQLite is used automatically when Azure SQL credentials are not configured.

### API Proxy
The frontend proxies `/api/*` requests to the backend at `http://localhost:8000`. This is configured in `vite.config.ts`.

### HMR Warnings
WebSocket connection warnings in development are cosmetic and don't affect functionality.
