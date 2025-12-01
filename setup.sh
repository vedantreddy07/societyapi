#!/bin/bash

# Society Management System - Quick Setup Script
# This script automates the setup process

echo "======================================"
echo "Society Management System - Setup"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 14+${NC}"
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL is not installed. Please install PostgreSQL 12+${NC}"
    echo "On Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites found${NC}"
echo ""

# Database Configuration
echo "======================================"
echo "Database Configuration"
echo "======================================"
read -p "Enter database name [society_management]: " DB_NAME
DB_NAME=${DB_NAME:-society_management}

read -p "Enter database user [society_user]: " DB_USER
DB_USER=${DB_USER:-society_user}

read -sp "Enter database password: " DB_PASSWORD
echo ""

read -p "Enter database host [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Enter database port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo ""
echo "Setting up backend..."

# Backend Setup
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set environment variable
export DATABASE_URL="$DATABASE_URL"

# Initialize database
echo "Initializing database..."
python init_db.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend setup complete${NC}"
else
    echo -e "${RED}✗ Backend setup failed${NC}"
    exit 1
fi

cd ..

# Frontend Setup
echo ""
echo "Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend setup complete${NC}"
else
    echo -e "${RED}✗ Frontend setup failed${NC}"
    exit 1
fi

cd ..

# Create start scripts
echo ""
echo "Creating start scripts..."

# Backend start script
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
python main.py
EOF

chmod +x start-backend.sh

# Frontend start script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm start
EOF

chmod +x start-frontend.sh

echo ""
echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Default Login Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "To start the application:"
echo "1. Start backend:  ./start-backend.sh"
echo "2. Start frontend: ./start-frontend.sh"
echo ""
echo "Access the application at: http://localhost:3000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}⚠️  Please change the default password after first login!${NC}"
echo ""
