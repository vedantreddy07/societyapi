# Deployment Guide

This guide covers both local and cloud deployment options for the Society Management System.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Cloud Deployment](#cloud-deployment)
3. [Environment Variables](#environment-variables)
4. [Security Considerations](#security-considerations)

## Local Deployment

### Option 1: Development Setup

**Prerequisites:**
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

**Step 1: Database Setup**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

In PostgreSQL console:
```sql
CREATE DATABASE society_management;
CREATE USER society_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE society_management TO society_user;
\q
```

Import schema:
```bash
psql -U society_user -d society_management -f backend/schema.sql
```

**Step 2: Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# Or Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set database URL
export DATABASE_URL="postgresql://society_user:your_password@localhost:5432/society_management"

# Initialize database with default admin
python init_db.py

# Run server
python main.py
```

Backend runs at: http://localhost:8000
Swagger docs: http://localhost:8000/docs

**Step 3: Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

Frontend runs at: http://localhost:3000

### Option 2: Production Local Setup

**Using Gunicorn (Backend)**
```bash
cd backend

# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

**Build Frontend for Production**
```bash
cd frontend

# Build
npm run build

# Serve using a simple HTTP server
npm install -g serve
serve -s build -l 3000
```

## Cloud Deployment

### Backend Deployment Options

#### Option 1: Heroku

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**
```bash
cd backend

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Deploy
git push heroku main

# Initialize database
heroku run python init_db.py

# Check logs
heroku logs --tail
```

Your API will be available at: `https://your-app-name.herokuapp.com`

#### Option 2: AWS EC2

**Launch EC2 Instance:**
1. Launch Ubuntu 20.04 LTS instance
2. Configure security group (allow ports 22, 80, 8000)
3. Connect to instance via SSH

**Setup on EC2:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y

# Clone/upload your code
# Setup PostgreSQL (as in local setup)

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd service
sudo nano /etc/systemd/system/society-backend.service
```

Service file content:
```ini
[Unit]
Description=Society Management Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/society-management/backend
Environment="DATABASE_URL=postgresql://society_user:password@localhost:5432/society_management"
ExecStart=/home/ubuntu/society-management/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable society-backend
sudo systemctl start society-backend
```

#### Option 3: DigitalOcean App Platform

1. Create new app from GitHub repository
2. Select backend folder
3. Configure build command: `pip install -r requirements.txt`
4. Configure run command: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add PostgreSQL database
6. Set environment variable `DATABASE_URL`

### Frontend Deployment Options

#### Option 1: Vercel

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Add environment variable
vercel env add REACT_APP_API_URL production
# Enter your backend URL
```

#### Option 2: Netlify

```bash
cd frontend

# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=build

# Set environment variables in Netlify dashboard:
# REACT_APP_API_URL = your-backend-url
```

#### Option 3: AWS S3 + CloudFront

```bash
# Build
npm run build

# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create S3 bucket
aws s3 mb s3://your-bucket-name

# Enable static website hosting
aws s3 website s3://your-bucket-name --index-document index.html

# Upload files
aws s3 sync build/ s3://your-bucket-name

# Set bucket policy for public access
```

#### Option 4: Same Server as Backend (Nginx)

If deploying on EC2/VPS with backend:

```bash
# Build frontend
cd frontend
npm run build

# Copy to nginx directory
sudo cp -r build/* /var/www/html/

# Configure nginx
sudo nano /etc/nginx/sites-available/society-management
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/html;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/society-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Variables

### Backend
Create `.env` file in backend directory:
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend
Create `.env` file in frontend directory:
```env
REACT_APP_API_URL=https://your-backend-url.com
```

## Security Considerations

### Production Checklist

**Backend:**
- [ ] Change default admin password
- [ ] Use strong SECRET_KEY (generate with: `openssl rand -hex 32`)
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly (remove wildcard in production)
- [ ] Use environment variables for sensitive data
- [ ] Enable database SSL connection
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates
- [ ] Database backups

**Frontend:**
- [ ] Use HTTPS
- [ ] Configure CSP headers
- [ ] Minify and optimize build
- [ ] Remove console.logs in production
- [ ] Implement proper error handling

### SSL/HTTPS Setup

**Using Let's Encrypt (Free):**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Database Backup

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/var/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U society_user society_management > $BACKUP_DIR/backup_$DATE.sql
# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Add to crontab:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

## Monitoring

**Using PM2 for Backend (Node alternative):**
```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
pm2 ecosystem

# Edit ecosystem.config.js
# Start application
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

**Logging:**
```bash
# View backend logs
pm2 logs

# Or with systemd
journalctl -u society-backend -f
```

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Use managed database service (RDS, CloudSQL)
- Implement Redis for session management

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes
- Enable caching

## Troubleshooting

**Database Connection Issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U society_user -d society_management -h localhost

# View logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

**Backend Not Starting:**
```bash
# Check Python version
python --version

# Verify all packages installed
pip list

# Check environment variables
echo $DATABASE_URL

# Run in debug mode
uvicorn main:app --reload --log-level debug
```

**Frontend Build Issues:**
```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version
```

## Support

For deployment issues, refer to:
- FastAPI documentation: https://fastapi.tiangolo.com/deployment/
- React deployment: https://create-react-app.dev/docs/deployment/
- PostgreSQL guides: https://www.postgresql.org/docs/
