# 3-Tier Deployment Guide

This guide explains how to deploy the Resource Management System in a 3-tier architecture on Azure.

## Architecture Overview

```
┌─────────────────────┐
│   Frontend (VM 1)   │
│   Static Files      │
│   Nginx Server      │
└──────────┬──────────┘
           │
           │ HTTP/HTTPS
           ▼
┌─────────────────────┐
│   Backend (VM 2)    │
│   Python FastAPI    │
│   Port 8000         │
└──────────┬──────────┘
           │
           │ SQL Connection
           ▼
┌─────────────────────┐
│  Azure SQL Database │
│   Managed Service   │
└─────────────────────┘
```

## Part 1: Azure SQL Database Setup

### Step 1: Create Azure SQL Database
1. Go to Azure Portal → Create Resource → SQL Database
2. Configure:
   - **Resource Group**: Create new or use existing
   - **Database Name**: `resource-management-db`
   - **Server**: Create new server
   - **Pricing Tier**: Choose appropriate tier (Basic/Standard/Premium)

### Step 2: Configure Firewall Rules
1. Go to your SQL Server → Networking
2. Add firewall rules:
   - Add client IP (for your development machine)
   - Add Backend VM IP (once created)
   - Add Frontend VM IP (if needed)

### Step 3: Run Database Schema
1. Connect to Azure SQL using SQL Server Management Studio or Azure Data Studio
2. Run the script: `backend/azure_sql_schema.sql`
3. Verify tables are created: `users`, `theme_config`

## Part 2: Backend Deployment (VM 2 - Python API)

### Create Ubuntu VM
1. Azure Portal → Virtual Machines → Create
2. Configuration:
   - **OS**: Ubuntu 22.04 LTS
   - **Size**: Standard_B2s (2 vCPUs, 4 GB RAM) minimum
   - **Ports**: Open port 8000 (or use nginx reverse proxy on 80/443)
   - **Authentication**: SSH key

### Install Dependencies
```bash
# SSH into the VM
ssh azureuser@<backend-vm-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install SQL Server ODBC Driver
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
sudo apt-get install -y unixodbc-dev
```

### Deploy Backend Code
```bash
# Clone your repository (or upload files)
git clone <your-repo-url>
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
nano .env
```

**.env file:**
```
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=resource-management-db
AZURE_SQL_USERNAME=your-admin-username
AZURE_SQL_PASSWORD=your-password
AZURE_SQL_DRIVER=ODBC Driver 18 for SQL Server
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://<frontend-vm-ip>
```

### Set up as System Service
```bash
sudo nano /etc/systemd/system/resource-api.service
```

```ini
[Unit]
Description=Resource Management FastAPI Backend
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/backend
Environment="PATH=/home/azureuser/backend/venv/bin"
EnvironmentFile=/home/azureuser/backend/.env
ExecStart=/home/azureuser/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable resource-api
sudo systemctl start resource-api
sudo systemctl status resource-api
```

### Configure Nginx (Optional but Recommended)
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/resource-api
```

```nginx
server {
    listen 80;
    server_name <backend-vm-ip-or-domain>;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/resource-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Part 3: Frontend Deployment (VM 1 - Static Files)

### Create Ubuntu VM
1. Azure Portal → Virtual Machines → Create
2. Configuration:
   - **OS**: Ubuntu 22.04 LTS
   - **Size**: Standard_B1s (1 vCPU, 1 GB RAM) minimum
   - **Ports**: Open ports 80 and 443
   - **Authentication**: SSH key

### Install Node.js and Build Frontend
```bash
# SSH into the VM
ssh azureuser@<frontend-vm-ip>

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone your repository
git clone <your-repo-url>
cd <your-repo>

# Update backend API URL in frontend
nano client/src/config/api.ts
```

**Update API URL:**
```typescript
export const API_BASE_URL = 'http://<backend-vm-ip>:8000';
```

**Build the frontend:**
```bash
# Install dependencies
npm install

# Build for production
npm run build
# This creates dist/public/ folder
```

### Install and Configure Nginx
```bash
sudo apt install nginx -y

# Copy build files to nginx directory
sudo cp -r dist/public/* /var/www/html/

# Configure nginx
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;

    server_name _;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (optional - if you want to avoid CORS)
    location /api {
        proxy_pass http://<backend-vm-ip>:8000/api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Part 4: Testing the Deployment

### Test Backend API
```bash
curl http://<backend-vm-ip>:8000/health
# Should return: {"status":"healthy"}

curl http://<backend-vm-ip>:8000/api/theme/
# Should return theme configurations
```

### Test Frontend
Open browser: `http://<frontend-vm-ip>`

You should see the login page.

### Test End-to-End
1. Create a user via signup
2. Login
3. Navigate through the application
4. Check if all features work

## Security Checklist

- [ ] Change default SSH ports
- [ ] Configure UFW firewall
- [ ] Enable HTTPS with Let's Encrypt
- [ ] Use Azure Key Vault for secrets
- [ ] Enable Azure SQL firewall rules
- [ ] Set up monitoring and alerts
- [ ] Configure backup for Azure SQL
- [ ] Use private networking (VNet) between VMs
- [ ] Implement rate limiting
- [ ] Enable logging and monitoring

## Monitoring Commands

### Backend VM
```bash
# Check API status
sudo systemctl status resource-api

# View logs
sudo journalctl -u resource-api -f

# Check nginx
sudo systemctl status nginx
```

### Frontend VM
```bash
# Check nginx
sudo systemctl status nginx

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Backend not connecting to Azure SQL
- Check firewall rules
- Verify connection string
- Test with: `telnet <server>.database.windows.net 1433`

### Frontend can't reach Backend
- Check CORS configuration in backend
- Verify backend VM firewall
- Check API_BASE_URL in frontend

### 502 Bad Gateway
- Check if backend service is running
- Verify nginx proxy configuration
- Check backend port availability

## Cost Optimization
- Use Azure Reserved Instances for VMs
- Choose appropriate SQL Database tier
- Set up auto-shutdown for non-production VMs
- Use Azure CDN for frontend static files
- Enable Azure SQL auto-pause for dev/test environments
