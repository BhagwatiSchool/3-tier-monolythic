#!/bin/bash
# Frontend VM Deployment Script
# Run this on Frontend VM (52.138.183.170)

set -e

echo "🚀 Deploying Frontend to $(hostname -I)"

# 1. Build (if code available)
if [ -d "frontend" ]; then
    echo "📦 Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

# 2. Deploy built files
echo "📁 Deploying files to /var/www/html..."
sudo cp -r frontend/dist/public/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html

# 3. Copy nginx config
echo "⚙️  Configuring nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/default

# 4. Test nginx
sudo nginx -t || { echo "❌ Nginx config error!"; exit 1; }

# 5. Restart nginx
sudo systemctl restart nginx

echo "✅ Frontend deployed successfully!"
echo "🌐 Visit: http://$(hostname -I | awk '{print $1}')/auth"
