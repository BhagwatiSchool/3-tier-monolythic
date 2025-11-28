# Deployment Guide

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
```

### 3. Configure Nginx
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/default

# Test nginx config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 4. Verify
```bash
# Should show "healthy"
curl http://localhost/health
```

---

## Backend VM Deployment (4.210.68.49)

### 1. Setup Environment
```bash
cd backend

# Create .env with Azure SQL credentials
cat > .env << EOF
AZURE_SQL_SERVER=ritserver
AZURE_SQL_USERNAME=your_username
AZURE_SQL_PASSWORD=your_password
AZURE_SQL_DATABASE=resource_management
EOF
```

### 2. Install & Run
```bash
pip install -r requirements.txt
python run.py
```

The backend will automatically detect Azure SQL credentials and connect!

---

## Troubleshooting

### Frontend shows 404
- Verify files are in `/var/www/html`: `ls /var/www/html/index.html`
- Check nginx config: `sudo nginx -t`
- Check nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Backend connection fails
- Verify Azure SQL firewall rules have your VM IP
- Check .env file has correct credentials
- Test: `curl http://localhost:8000/api/health`

### API calls return 404
- Ensure backend is running on port 8000
- Check nginx proxy config includes `/api/` location block
- Test: `curl http://localhost/api/health` from frontend VM
