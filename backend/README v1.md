# Resource Management Dashboard - Complete Deployment Guide

> **3-Tier Azure Architecture**: Frontend (React) + Backend (Python FastAPI) + Azure SQL Database

This guide will take you from **ZERO to FULL PRODUCTION** deployment on Azure VMs. Follow step-by-step!

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Architecture](#-architecture)
3. [Tech Stack](#-tech-stack)
4. [Prerequisites](#-prerequisites)
5. [Local Development Setup (Windows)](#-local-development-setup-windows)
6. [Backend Deployment on Ubuntu VM](#-backend-deployment-on-ubuntu-vm)
7. [Frontend Deployment on Ubuntu VM](#-frontend-deployment-on-ubuntu-vm)
8. [Azure SQL Database Setup](#-azure-sql-database-setup)
9. [Testing & Verification](#-testing--verification)
10. [Troubleshooting](#-troubleshooting)
11. [Production Checklist](#-production-checklist)

---

## 🎯 Project Overview

A modern resource management dashboard converted from Lovable to 3-tier Azure architecture:

- **Frontend**: React 18 + TypeScript + Vite + Shadcn UI
- **Backend**: Python FastAPI + SQLAlchemy
- **Database**: Azure SQL Database

**Deployment Target**: Separate Azure Ubuntu VMs for frontend and backend.

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   Frontend VM       │
│   (Ubuntu)          │
│   React + Vite      │
│   Port: 5000        │
└──────────┬──────────┘
           │
           │ HTTP API Calls
           ▼
┌─────────────────────┐
│   Backend VM        │
│   (Ubuntu)          │
│   FastAPI + Python  │
│   Port: 8000        │
└──────────┬──────────┘
           │
           │ SQL Connection
           ▼
┌─────────────────────┐
│   Azure SQL         │
│   ritserver         │
│   Port: 1433        │
└─────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **Shadcn UI** + Tailwind CSS
- **React Query** for data fetching
- **Wouter** for routing

### Backend
- **Python 3.11** (Required for Windows compatibility)
- **FastAPI** web framework
- **SQLAlchemy** ORM
- **PyMSSQL** for Azure SQL connection
- **JWT** for authentication
- **Uvicorn/Gunicorn** for production server

### Database
- **Azure SQL Database**
- Auto-migrations via SQLAlchemy
- Connection pooling enabled

---

## ✅ Prerequisites

### For Local Development (Windows)
- ✅ Python 3.11 (NOT 3.13) - [Download here](https://www.python.org/downloads/release/python-3110/)
- ✅ Node.js 18+ - [Download here](https://nodejs.org/)
- ✅ Git - [Download here](https://git-scm.com/)
- ✅ Code Editor (VS Code recommended)

### For Azure Deployment
- ✅ 2 Ubuntu VMs (20.04 or 22.04)
  - VM 1: Backend (2 CPU, 4GB RAM minimum)
  - VM 2: Frontend (1 CPU, 2GB RAM minimum)
- ✅ Azure SQL Database created
- ✅ SSH access to both VMs
- ✅ Firewall rules configured

---

## 💻 Local Development Setup (Windows)

### Step 1: Clone the Repository

```powershell
# Clone your project
git clone <your-repo-url>
cd your-project-folder
```

### Step 2: Backend Setup (Python)

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment (IMPORTANT!)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt now

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 sqlalchemy-2.0.23 ...
```

### Step 3: Configure Backend Environment

Create `backend/.env` file:

```env
DATABASE_URL=mssql+pymssql://ritserver@ritserver:Ritesh@12345@ritserver.database.windows.net:1433/ritserver
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5000
```

### Step 4: Start Backend Server

```powershell
# Make sure you're in backend folder with (venv) active
python run.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running!** Test: Open browser → `http://localhost:8000/health`

### Step 5: Frontend Setup (React)

Open **NEW PowerShell terminal** (keep backend running):

```powershell
# Go to project root (NOT client folder!)
cd your-project-folder

# Install dependencies
npm install

# Start frontend development server
npm run dev
```

**Expected Output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5000/
  ➜  Network: use --host to expose
```

✅ **Frontend is running!** Open browser → `http://localhost:5000`

You should see: **"Frontend is Working! 🎉"**

---

## 🚀 Backend Deployment on Ubuntu VM

### Step 1: Connect to Backend VM

```bash
# SSH into your Ubuntu VM
ssh user@your-backend-vm-ip

# Example:
# ssh ritesh@20.123.45.67
```

### Step 2: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y build-essential python3.11 python3.11-venv python3-pip unixodbc-dev git

# Verify Python version
python3.11 --version
# Should show: Python 3.11.x
```

### Step 3: Transfer Backend Code to VM

**Option A: Using SCP (from Windows PowerShell)**
```powershell
# From your Windows machine
scp -r "E:\path\to\backend" user@vm-ip:/home/user/
```

**Option B: Using Git (on Ubuntu VM)**
```bash
# On Ubuntu VM
cd /home/user
git clone <your-repo-url>
cd your-repo/backend
```

### Step 4: Create Virtual Environment

```bash
# Navigate to backend folder
cd /home/user/backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in prompt
```

### Step 5: Install Python Dependencies

```bash
# Make sure (venv) is active!
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed fastapi uvicorn sqlalchemy pymssql ...
```

### Step 6: Create Environment Configuration

```bash
# Create environment file
sudo nano /etc/resource-backend.env
```

**Add this content:**
```env
DATABASE_URL=mssql+pymssql://ritserver@ritserver:Ritesh@12345@ritserver.database.windows.net:1433/ritserver
SECRET_KEY=your-production-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://your-frontend-vm-ip:5000
```

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### Step 7: Test Backend Manually First

```bash
# Make sure you're in backend folder with venv active
source venv/bin/activate
python run.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it:**
```bash
# In another terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

If working, press `Ctrl+C` to stop. Now create systemd service!

### Step 8: Create Systemd Service (Auto-start)

```bash
# Create service file
sudo nano /etc/systemd/system/resource-backend.service
```

**Add this content:**
```ini
[Unit]
Description=Resource Management Backend API
After=network.target

[Service]
Type=notify
User=ritesh
WorkingDirectory=/home/ritesh/backend
Environment="PATH=/home/ritesh/backend/venv/bin"
EnvironmentFile=/etc/resource-backend.env
ExecStart=/home/ritesh/backend/venv/bin/gunicorn app.main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `ritesh` with your actual username!

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### Step 9: Install Gunicorn

```bash
# Activate venv and install gunicorn
source /home/ritesh/backend/venv/bin/activate
pip install gunicorn
```

### Step 10: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable resource-backend

# Start service
sudo systemctl start resource-backend

# Check status
sudo systemctl status resource-backend
```

**Expected Output:**
```
● resource-backend.service - Resource Management Backend API
   Loaded: loaded (/etc/systemd/system/resource-backend.service; enabled)
   Active: active (running) since ...
```

### Step 11: Configure Firewall

```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Check firewall status
sudo ufw status
```

### Step 12: Test External Access

**From your Windows laptop:**
```powershell
# Test health endpoint
curl http://YOUR-BACKEND-VM-IP:8000/health

# Should return: {"status":"healthy"}
```

✅ **Backend Deployment Complete!**

---

## 🎨 Frontend Deployment on Ubuntu VM

### Step 1: Connect to Frontend VM

```bash
# SSH into your frontend VM
ssh user@your-frontend-vm-ip
```

### Step 2: Install Node.js

```bash
# Update packages
sudo apt update

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version  # Should show v18.x.x
npm --version   # Should show 9.x.x
```

### Step 3: Transfer Frontend Code

**Option A: Using SCP (from Windows)**
```powershell
scp -r "E:\path\to\your-project" user@frontend-vm-ip:/home/user/
```

**Option B: Using Git (on VM)**
```bash
cd /home/user
git clone <your-repo-url>
```

### Step 4: Install Dependencies

```bash
# Navigate to project root
cd /home/user/your-project

# Install dependencies
npm install
```

### Step 5: Configure Frontend Environment

```bash
# Create .env file in project root
nano .env
```

**Add this:**
```env
VITE_API_URL=http://YOUR-BACKEND-VM-IP:8000
```

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### Step 6: Build Frontend

```bash
# Build production files
npm run build
```

**Expected Output:**
```
vite v5.0.0 building for production...
✓ built in 15.23s
```

This creates `client/dist/` folder with production files.

### Step 7: Install and Configure Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/resource-frontend
```

**Add this configuration:**
```nginx
server {
    listen 5000;
    server_name _;
    
    root /home/ritesh/your-project/client/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Important:** Replace `/home/ritesh/your-project` with your actual path!

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### Step 8: Enable Nginx Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/resource-frontend /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Should show: nginx: configuration file /etc/nginx/nginx.conf test is successful

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx on boot
sudo systemctl enable nginx
```

### Step 9: Configure Firewall

```bash
# Allow port 5000
sudo ufw allow 5000/tcp

# Check status
sudo ufw status
```

### Step 10: Test Frontend Access

**From your Windows laptop browser:**

Open: `http://YOUR-FRONTEND-VM-IP:5000`

You should see: **"Frontend is Working! 🎉"**

✅ **Frontend Deployment Complete!**

---

## 🗄️ Azure SQL Database Setup

### Step 1: Create Azure SQL Database

1. Go to **Azure Portal** → Create Resource
2. Search **"SQL Database"** → Create
3. **Settings:**
   - Server: `ritserver.database.windows.net`
   - Database: `ritserver`
   - Username: `ritserver@ritserver`
   - Password: `Ritesh@12345`

### Step 2: Configure Firewall Rules

1. Go to your SQL Server → **Networking**
2. Add firewall rules:
   - Add your **Backend VM IP**
   - Add your **local IP** (for testing)

### Step 3: Test Connection

**From Backend VM:**
```bash
# Install SQL client for testing
pip install pymssql

# Test connection
python3 << EOF
import pymssql
conn = pymssql.connect(
    server='ritserver.database.windows.net',
    user='ritserver@ritserver',
    password='Ritesh@12345',
    database='ritserver'
)
print("✅ Connected to Azure SQL!")
conn.close()
EOF
```

---

## ✅ Testing & Verification

### Backend Health Check

```bash
# Test from anywhere
curl http://BACKEND-VM-IP:8000/health

# Expected: {"status":"healthy"}
```

### Database Connection Check

```bash
# Test database tables
curl http://BACKEND-VM-IP:8000/api/users
```

### Frontend-Backend Integration

1. Open browser: `http://FRONTEND-VM-IP:5000`
2. Try login/signup
3. Check browser console (F12) for errors
4. Verify API calls go to backend VM

### Service Status Commands

```bash
# Backend service
sudo systemctl status resource-backend
sudo journalctl -u resource-backend -f  # Live logs

# Frontend (Nginx)
sudo systemctl status nginx
sudo tail -f /var/log/nginx/access.log  # Access logs
sudo tail -f /var/log/nginx/error.log   # Error logs
```

---

## 🔧 Troubleshooting

### Problem 1: Backend not starting

**Error:** `externally-managed-environment`

**Solution:**
```bash
# Make sure you created virtual environment!
cd /home/user/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Problem 2: Can't connect to Azure SQL

**Error:** `Cannot open server 'ritserver' requested by the login`

**Solution:**
1. Check Azure SQL firewall rules
2. Add your VM's public IP
3. Verify connection string in `/etc/resource-backend.env`

---

### Problem 3: Frontend shows blank page

**Solution:**
```bash
# Check browser console (F12)
# Verify .env has correct backend URL
nano .env
# Should have: VITE_API_URL=http://BACKEND-IP:8000

# Rebuild frontend
npm run build
sudo systemctl restart nginx
```

---

### Problem 4: Service keeps crashing

```bash
# Check logs
sudo journalctl -u resource-backend -n 100

# Common issues:
# - Wrong path in service file
# - Database connection failed
# - Port already in use
```

---

### Problem 5: Port already in use

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Restart service
sudo systemctl restart resource-backend
```

---

## 📝 Production Checklist

### Security
- [ ] Change `SECRET_KEY` in production
- [ ] Use strong Azure SQL password
- [ ] Enable HTTPS (SSL certificates)
- [ ] Configure CORS properly
- [ ] Set up Azure Key Vault for secrets

### Performance
- [ ] Enable Nginx caching
- [ ] Configure Gunicorn workers (CPU count × 2 + 1)
- [ ] Set up database connection pooling
- [ ] Enable gzip compression

### Monitoring
- [ ] Set up logging (journald or file-based)
- [ ] Configure log rotation
- [ ] Set up Azure Monitor alerts
- [ ] Track API response times

### Backup
- [ ] Enable Azure SQL automated backups
- [ ] Create VM snapshots
- [ ] Backup environment files
- [ ] Document configuration changes

---

## 🎉 Success!

Your 3-tier application is now fully deployed on Azure!

**Architecture:**
```
Frontend VM (Port 5000) → Backend VM (Port 8000) → Azure SQL (Port 1433)
```

**Quick Commands Reference:**

```bash
# Backend service
sudo systemctl status resource-backend    # Check status
sudo systemctl restart resource-backend   # Restart
sudo journalctl -u resource-backend -f    # Live logs

# Frontend (Nginx)
sudo systemctl status nginx               # Check status
sudo systemctl restart nginx              # Restart
sudo tail -f /var/log/nginx/access.log   # Access logs
```

---

## 📞 Support

If you encounter issues:
1. Check logs: `sudo journalctl -u resource-backend -n 100`
2. Verify firewall: `sudo ufw status`
3. Test connectivity: `curl http://localhost:8000/health`
4. Check environment variables: `cat /etc/resource-backend.env`

**Happy Deploying! 🚀**
