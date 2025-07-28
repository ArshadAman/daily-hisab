#!/bin/bash

# Configuration
DOMAIN="dailyhisaab.deltospark.com"
EMAIL="arshadaman202@gmail.com"  # Replace with your email
STAGING=0  # Set to 1 for testing

echo "🔒 Setting up SSL certificates for Django business accounting app..."

# Create directories
mkdir -p certbot/conf certbot/www

# Download recommended TLS parameters
if [ ! -e "certbot/conf/options-ssl-nginx.conf" ]; then
    echo "📥 Downloading TLS parameters..."
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "certbot/conf/options-ssl-nginx.conf"
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "certbot/conf/ssl-dhparams.pem"
fi

# Start nginx with HTTP only
echo "🚀 Starting nginx (HTTP only)..."
docker-compose up -d nginx

# Get SSL certificate
echo "🔐 Requesting SSL certificate for $DOMAIN..."

if [ $STAGING == 1 ]; then
    STAGING_FLAG="--staging"
else
    STAGING_FLAG=""
fi

docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    $STAGING_FLAG \
    -d $DOMAIN

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained successfully!"
    echo "🔄 Updating nginx configuration for HTTPS..."
    
    # Create HTTPS nginx config
    cat > nginx/default.conf << 'EOF'
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name dailyhisaab.deltospark.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name dailyhisaab.deltospark.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/dailyhisaab.deltospark.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dailyhisaab.deltospark.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # API endpoints for accounting app
    location /api/ {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # API-specific headers
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Django admin
    location /admin/ {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Main application
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (CSS, JS, images)
    location /static/ {
        alias /var/www/html/static/;
        expires 1y;
        access_log off;
        add_header Cache-Control "public, immutable";
        
        # Gzip compression for static files
        gzip_static on;
        gzip_vary on;
    }

    # Media files (uploaded documents, receipts)
    location /media/ {
        alias /var/www/html/media/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public";
        
        # Security for uploaded files
        add_header X-Content-Type-Options nosniff always;
    }
}
EOF

    # Reload nginx
    docker-compose exec nginx nginx -s reload
    echo "🎉 SSL setup complete! Your Django accounting app is now secured."
    
else
    echo "❌ Failed to obtain SSL certificate. Check your domain DNS settings."
fi