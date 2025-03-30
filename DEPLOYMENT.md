# Deployment Guide

This document provides instructions for deploying the Oz Stack Starter Kit to various production environments.

## Preparing for Production

Before deploying to production, make these changes:

1. Create a production `.env` file:
   ```
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   ```

2. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. Build the CSS for production:
   ```bash
   npm run build:css
   ```

## Deployment Options

### Option 1: Basic Server Deployment

#### Requirements
- Linux server (Ubuntu/Debian recommended)
- Python 3.8+
- Node.js 14+
- Nginx (for reverse proxy)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/oz-stack-starterkit.git
   cd oz-stack-starterkit
   ```

2. Setup with production configuration:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   npm install
   npm run build:css
   ```

3. Create a production `.env` file with appropriate settings.

4. Set up a systemd service (recommended for auto-restart):
   ```
   [Unit]
   Description=Oz Stack Starter Kit
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/oz-stack-starterkit
   Environment="PATH=/path/to/oz-stack-starterkit/venv/bin"
   ExecStart=/path/to/oz-stack-starterkit/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

   Save this as `/etc/systemd/system/ozstack.service`

5. Enable and start the service:
   ```bash
   sudo systemctl enable ozstack
   sudo systemctl start ozstack
   ```

6. Configure Nginx as a reverse proxy:
   ```
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /path/to/oz-stack-starterkit/src/static/;
           expires 30d;
       }
   }
   ```

   Save this as `/etc/nginx/sites-available/ozstack` and create a symlink:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ozstack /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. Set up SSL with Certbot:
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

### Option 2: Docker Deployment

#### Requirements
- Docker
- Docker Compose (optional)

#### Steps

1. Create a `Dockerfile` in the project root:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Install Node.js
   RUN apt-get update && apt-get install -y \
       curl \
       gnupg \
       && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
       && apt-get install -y nodejs \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt gunicorn

   # Copy package.json and install Node.js dependencies
   COPY package.json .
   RUN npm install

   # Copy the rest of the application
   COPY . .

   # Build the CSS
   RUN npm run build:css

   # Expose port
   EXPOSE 8000

   # Run the application
   CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "src.main:app"]
   ```

2. Create a `.dockerignore` file:
   ```
   venv/
   node_modules/
   .git/
   .env
   __pycache__/
   *.pyc
   ```

3. Build and run the Docker container:
   ```bash
   docker build -t ozstack .
   docker run -d -p 80:8000 --name ozstack-app ozstack
   ```

4. (Optional) Create a `docker-compose.yml` file for easier management:
   ```yaml
   version: '3'

   services:
     web:
       build: .
       ports:
         - "80:8000"
       restart: always
       environment:
         - HOST=0.0.0.0
         - PORT=8000
         - DEBUG=False
   ```

   Then use:
   ```bash
   docker-compose up -d
   ```

### Option 3: Cloud Platform Deployment

#### Heroku

1. Create a `Procfile` in the project root:
   ```
   web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
   ```

2. Create a `runtime.txt` file:
   ```
   python-3.11.0
   ```

3. Deploy to Heroku:
   ```bash
   heroku create
   git push heroku main
   ```

4. Set environment variables:
   ```bash
   heroku config:set DEBUG=False
   ```

#### AWS Elastic Beanstalk

1. Install the EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize EB application:
   ```bash
   eb init
   ```

3. Create an EB environment:
   ```bash
   eb create
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

## Performance Optimization for Production

1. Enable Gzip compression in your web server:
   ```
   # Example for Nginx
   gzip on;
   gzip_comp_level 5;
   gzip_min_length 256;
   gzip_proxied any;
   gzip_vary on;
   gzip_types
     application/javascript
     application/json
     application/x-javascript
     text/css
     text/javascript
     text/plain;
   ```

2. Configure proper caching for static assets:
   ```
   # Example for Nginx
   location /static/ {
       alias /path/to/oz-stack-starterkit/src/static/;
       expires 30d;
       add_header Cache-Control "public, max-age=2592000";
   }
   ```

3. Use a CDN for static assets (optional):
   - CloudFront (AWS)
   - Cloudflare
   - Fastly

## Security Considerations

1. Set up HTTPS (covered in the Nginx + Certbot section above)

2. Secure headers (add to Nginx):
   ```
   add_header X-Content-Type-Options "nosniff";
   add_header X-Frame-Options "SAMEORIGIN";
   add_header X-XSS-Protection "1; mode=block";
   add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://unpkg.com; style-src 'self' 'unsafe-inline' https://unpkg.com";
   ```

3. Environment variables:
   - Never commit `.env` files to Git
   - Use different `.env` files for development and production
   - Consider using a secrets manager for production credentials

4. Regular updates:
   - Keep dependencies updated
   - Run `pip install -U -r requirements.txt` regularly
   - Run `npm update` regularly

## Monitoring and Logging

1. Add application logging:
   - Update main.py to include proper logging
   - Configure log rotation

2. Use monitoring tools:
   - Prometheus + Grafana
   - Datadog
   - New Relic

3. Setup alerts for:
   - High error rates
   - Excessive CPU/memory usage
   - Slow response times