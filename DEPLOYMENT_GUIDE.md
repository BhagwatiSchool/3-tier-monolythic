# Deployment Guide

## 🚀 Quick Deploy (Automated Scripts)

### Frontend VM - One Command Deploy
```bash
# On Frontend VM (52.138.183.170):
bash deploy-frontend.sh
```
✅ Automatically:
- Builds frontend
- Copies files to nginx
- Configures nginx with proper routing
- Restarts services

### Backend VM - One Command Deploy
```bash
# On Backend VM (4.210.68.49):
bash deploy-backend.sh
```
✅ Automatically:
- Sets up Python venv
- Installs dependencies
- Starts backend on port 8000

---

## Frontend VM Deployment (52.138.183.170)

### 1. Build the Frontend
```bash
cd frontend
npm install
npm run build
```

### 2. Deploy Built Files
```bash
# Copy built files to nginx root
sudo cp -r frontend/dist/public/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html

# Verify index.html is there
ls -la /var/www/html/index.html
```

### 3. Configure Nginx
```bash
# Copy nginx config from project root
sudo cp nginx.conf /etc/nginx/sites-available/default

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Check nginx is running
sudo systemctl status nginx
```

### 4. Verify Deployment
```bash
# Should show "healthy"
curl http://localhost/health

# Should show login page HTML
curl http://localhost/ | head -20

# Should proxy to backend
curl http://localhost/api/auth/login -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test"}'
```

---

## Backend VM Deployment (4.210.68.49)

### 1. Setup Python Environment
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional - for Azure SQL)
```bash
# Create .env with Azure SQL credentials (if using Azure SQL, not SQLite)
cat > .env << EOF
AZURE_SQL_SERVER=ritserver
AZURE_SQL_USERNAME=your_username
AZURE_SQL_PASSWORD=your_password
AZURE_SQL_DATABASE=resource_management
EOF
```

### 3. Run Backend
```bash
# Activate venv if not already
source venv/bin/activate

# Run server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Or use python run.py if run.py exists
python run.py
```

**Note:** Backend auto-detects environment:
- No .env = SQLite (default for testing)
- With .env = Azure SQL (production)

### 4. Verify Backend
```bash
# From another terminal:
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ritesh@apka.bhai","password":"Aagebadho"}'

# Should return JWT token
```

---

## Architecture

```
Frontend VM (52.138.183.170)
  └─ Nginx (Port 80)
       ├─ / → /var/www/html (React SPA)
       └─ /api/* → Backend VM:8000 (Proxy)

Backend VM (4.210.68.49)
  └─ FastAPI (Port 8000)
       ├─ SQLite (default, for testing)
       └─ Azure SQL (if .env configured)
```

---

## Troubleshooting

### Frontend shows 404 for /auth or /resources
**Solution:** React SPA routing needs `try_files $uri $uri/ /index.html;` in nginx
- Check nginx config: `sudo nginx -t`
- Verify line exists: `sudo grep -n "try_files" /etc/nginx/sites-available/default`

### API returns 404 from frontend
**Solution:** Nginx proxy may not be configured
- Check config: `sudo grep -A10 "location /api/" /etc/nginx/sites-available/default`
- Verify backend is running: `curl http://4.210.68.49:8000/api/auth/login`
- Test proxy manually: `curl http://localhost/api/auth/login` from frontend VM
- Check nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Backend not starting
- Check Python/pip: `python3 --version`
- Verify dependencies: `pip list | grep fastapi`
- Check port 8000 not in use: `sudo lsof -i :8000`

### Backend connection refused
**Solution:** Firewall or IP mismatch
- Verify backend IP: `hostname -I`
- Update nginx config if IP changed: `sudo nano /etc/nginx/sites-available/default`
- Nginx upstream should match backend VM IP (currently: 4.210.68.49)
