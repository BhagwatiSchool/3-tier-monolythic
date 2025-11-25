# 🚀 Azure Deployment Guide

Complete step-by-step guide to deploy this React dashboard on Azure VM.

## 📋 Prerequisites

✅ Azure VM (Ubuntu 20.04+): **128.251.9.205**  
✅ Python FastAPI Backend running on: **134.149.43.65:8000**  
✅ Node.js 18+ installed on local machine  
✅ SSH access to Azure VM

---

## 🔨 Step 1: Build the Frontend

On your **local machine**:

```bash
cd client-new

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in: dist/public/
```

**What happens:**
- TypeScript compiled to JavaScript
- Vite bundles all files
- Assets optimized and minified
- Final size: ~800KB (optimized)

---

## 📦 Step 2: Transfer Files to Azure VM

### Option A: Using SCP (Secure Copy)

```bash
# From client-new folder on your machine
scp -r dist/public/* azureuser@128.251.9.205:/var/www/dashboard/
```

### Option B: Using Git

```bash
# On Azure VM
cd /var/www
git clone <your-repo-url> dashboard
cd dashboard/client-new
npm install
npm run build
```

---

## 🌐 Step 3: Install Nginx on Azure VM

SSH into your Azure VM:

```bash
ssh azureuser@128.251.9.205
```

Install Nginx:

```bash
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## ⚙️ Step 4: Configure Nginx

Create Nginx config file:

```bash
sudo nano /etc/nginx/sites-available/dashboard
```

Paste this configuration:

```nginx
server {
    listen 80;
    server_name 128.251.9.205;

    # Root directory
    root /var/www/dashboard/dist/public;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_min_length 256;

    # Serve static assets directly
    location /assets/ {
        try_files $uri =404;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy to Python backend
    location /api/ {
        proxy_pass http://134.149.43.65:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # SPA fallback - all other routes go to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

---

## 🔐 Step 5: Configure Firewall

Allow HTTP traffic:

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 22  # SSH
sudo ufw enable
```

---

## ✅ Step 6: Verify Deployment

### Test Nginx:
```bash
curl http://134.149.43.65
```

### Test from your browser:
```
http://128.251.9.205
```

### Check logs if issues:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

---

## 🔄 Update Deployment (Future Changes)

When you make changes:

```bash
# 1. Build locally
cd client-new
npm run build

# 2. Transfer to VM
scp -r dist/public/* azureuser@128.251.9.205:/var/www/dashboard/

# 3. Reload Nginx (on VM)
sudo systemctl reload nginx
```

---

## 🐛 Troubleshooting

### Issue: "Cannot GET /"
**Solution:** Check Nginx root path
```bash
ls -la /var/www/dashboard/dist/public/
# Should show index.html and assets/
```

### Issue: CSS/JS not loading
**Solution:** Clear browser cache or check assets path
```bash
curl http://128.251.9.205/assets/index-abc123.js
```

### Issue: API calls failing
**Solution:** Check backend connectivity
```bash
curl http://134.149.43.65:8000/health
```

### Issue: 404 on page refresh
**Solution:** Ensure Nginx SPA config is correct
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

---

## 🔒 Optional: Add HTTPS (SSL)

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Get SSL certificate (requires domain name):

```bash
sudo certbot --nginx -d yourdomain.com
```

For IP-only deployment, use self-signed certificate:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt
```

---

## 📊 Monitoring

Check service status:

```bash
sudo systemctl status nginx
```

Monitor real-time logs:

```bash
sudo tail -f /var/log/nginx/access.log
```

---

## 🎯 Success Checklist

- [ ] Frontend builds without errors (`npm run build`)
- [ ] Files transferred to `/var/www/dashboard/dist/public/`
- [ ] Nginx installed and running
- [ ] Nginx config created and enabled
- [ ] Firewall allows HTTP (port 80)
- [ ] Can access http://128.251.9.205 in browser
- [ ] Login/signup works (connects to Python backend)
- [ ] Dashboard page loads with data

---

## 📞 Support

If you encounter issues:
1. Check Nginx error logs
2. Verify Python backend is running
3. Test API endpoints directly
4. Check browser console for errors

**Your deployment should now be live! 🚀**
