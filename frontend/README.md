# Resource Management Dashboard - Frontend

Modern React dashboard application for managing Azure resources, built with TypeScript, Vite, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ or Bun
- Python FastAPI backend running on `http://134.149.43.65:8000`

### Installation

```bash
# Install dependencies
npm install

# Or use Bun (faster)
bun install
```

### Development

```bash
# Start development server (runs on http://134.149.43.65:5000)
npm run dev

# Or with Bun
bun run dev
```

### Production Build

```bash
# Build for production
npm run build

# Output will be in: dist/public/
```

## 📁 Project Structure

```
client-new/
├── src/
│   ├── components/          # Reusable components
│   │   ├── ui/             # Shadcn UI components
│   │   ├── Layout.tsx      # Main app layout with navigation
│   │   └── ProtectedRoute.tsx
│   ├── contexts/           # React contexts
│   │   └── AuthContext.tsx # Authentication state management
│   ├── hooks/              # Custom React hooks
│   │   └── use-toast.ts
│   ├── lib/                # Utilities and API client
│   │   ├── api.ts          # Axios API client
│   │   └── utils.ts        # Helper functions
│   ├── pages/              # Route pages
│   │   ├── Auth.tsx        # Login/Signup page
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── Profile.tsx     # User profile
│   │   ├── Settings.tsx    # App settings
│   │   ├── ThemeSettings.tsx
│   │   ├── UserManagement.tsx
│   │   └── NotFound.tsx
│   ├── App.tsx             # Root component with routing
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles & theme variables
├── .env.development        # Dev environment variables
├── .env.production         # Production environment variables
├── package.json
├── vite.config.ts          # Vite configuration
└── tailwind.config.ts      # Tailwind CSS configuration
```

## 🔧 Configuration

### Environment Variables

Create `.env.production` file:

```env
VITE_API_URL=http://134.149.43.65:8000
VITE_ENVIRONMENT=production
```

### Python Backend API

The frontend expects these endpoints:

- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `GET /api/users` - Get all users (admin only)
- `GET /api/resources/stats` - Get resource statistics
- `GET /api/theme` - Get theme configuration
- `PUT /api/theme` - Update theme

## 🎨 Features

- **Authentication** - JWT-based login/signup
- **Dashboard** - Resource monitoring with charts
- **User Management** - Admin user/role management
- **Profile Management** - Update user information
- **Theme Settings** - Customizable appearance
- **Settings** - Application preferences
- **Responsive Design** - Mobile-friendly UI

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching & caching
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS
- **Shadcn UI** - Component library
- **Lucide Icons** - Icon library

## 📦 Building for Production

```bash
# Build the app
npm run build

# Output folder: dist/public/
# Deploy this folder to your Azure VM with Nginx
```

### Nginx Configuration (for Azure VM)

```nginx
server {
    listen 80;
    server_name 128.251.9.205;
    root /var/www/dashboard/dist/public;
    index index.html;

    # Serve assets directly
    location /assets/ {
        try_files $uri =404;
    }

    # SPA fallback - all other routes go to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Enable gzip
    gzip on;
    gzip_types text/css application/javascript application/json;
}
```

## 🔑 Authentication Flow

1. User logs in via `/auth` page
2. Backend returns JWT token + user object
3. Token stored in `localStorage`
4. Axios interceptor adds token to all requests
5. Protected routes check for valid token
6. On 401 error, user redirected to login

## 🐛 Troubleshooting

### "Cannot find module" errors
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build errors
```bash
npm run build -- --force
```

### API connection issues
- Check `VITE_API_URL` in `.env.production`
- Ensure Python backend is running
- Check CORS configuration on backend

## 📝 License

MIT

## 👨‍💻 Author

Built for Azure deployment with Python FastAPI backend integration.
