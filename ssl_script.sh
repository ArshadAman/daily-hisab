#!/bin/bash

DOMAIN="dailyhisaab.deltospark.com"
EMAIL="arshadaman202@gmail.com"  # Replace with your actual email
STAGING=1  # Set to 0 for production certificates

echo "🔒 Setting up SSL for Django business accounting app..."

# Ensure directories exist
mkdir -p certbot/conf certbot/www nginx

# Stop any running containers
docker-compose down

# Start only nginx and web (not certbot yet)
echo "🚀 Starting web services..."
docker-compose up -d web nginx

# Wait for services to be ready
sleep 10

# Test domain accessibility
echo "🌐 Testing domain accessibility..."
if curl -f http://$DOMAIN/ > /dev/null 2>&1; then
    echo "✅ Domain is accessible"
else
    echo "❌ Domain is not accessible. Please check:"
    echo "   - DNS settings for $DOMAIN"
    echo "   - Server firewall (port 80 must be open)"
    echo "   - Docker containers are running"
    docker-compose ps
    exit 1
fi

# Download TLS parameters if not exists
if [ ! -e "certbot/conf/options-ssl-nginx.conf" ]; then
    echo "📥 Downloading TLS parameters..."
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "certbot/conf/options-ssl-nginx.conf"
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "certbot/conf/ssl-dhparams.pem"
fi

# Get certificate
echo "🔐 Requesting SSL certificate..."

STAGING_FLAG=""
if [ $STAGING == 1 ]; then
    STAGING_FLAG="--staging"
    echo "⚠️  Using staging environment (test certificate)"
fi

docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    $STAGING_FLAG \
    -d $DOMAIN \
    --verbose

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained!"
    
    # Update nginx config for HTTPS
    cat > nginx/default.conf << EOF
# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name $DOMAIN;
    
    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files \$uri \$uri/ =404;
    }
    
    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://\$host\$request_uri;
    }
}

# HTTPS server for Django accounting app
server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # Security headers for business app
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # API endpoints for accounting operations
    location /api/ {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts for API calls
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Django admin interface
    location /admin/ {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Static files (CSS, JS, images)
    location /static/ {
        alias /var/www/html/static/;
        expires 1y;
        access_log off;
        add_header Cache-Control "public, immutable";
        gzip_static on;
    }

    # Media files (invoices, receipts, documents)
    location /media/ {
        alias /var/www/html/media/;
        expires 30d;
        access_log off;
        add_header Cache-Control "public";
        add_header X-Content-Type-Options nosniff;
    }
    
    # Main Django application
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Reload nginx with new config
    docker-compose exec nginx nginx -s reload
    
    echo "🎉 SSL setup complete for your Django accounting app!"
    echo "🌐 Your app is now available at: https://$DOMAIN"
    
else
    echo "❌ Certificate request failed. Run debug script first:"
    echo "   ./scripts/debug-ssl.sh"
fi