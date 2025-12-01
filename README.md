# Society Management System

A comprehensive web application for managing society operations including residents, maintenance, and vendors.

## Features

### 1. Multi-Level User Authentication
- **Admin**: Full system access
- **Accounts**: Manage maintenance and financial records
- **Operations**: Manage flats, residents, and vendors
- **Flat Owners**: View their flat details and maintenance

### 2. Resident Management
- Complete flat details (number, owner, size, type)
- Owner information (name, email, phone)
- Tenant history tracking with agreements
- Flat resident details management

### 3. Maintenance Management
- Automatic monthly maintenance generation
- 10% interest on overdue payments
- Invoice generation for all flats
- Receipt generation upon payment
- Payment status tracking (Paid, Pending, Overdue)

### 4. Vendor Management
- Vendor details and contact information
- Work status tracking (Active, Completed, On Hold)
- Financial tracking (total charges, paid amount, remaining)

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt

### Frontend
- **Framework**: React
- **HTTP Client**: Axios
- **Styling**: CSS3

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

## Installation & Setup

### Local Deployment

#### 1. Database Setup

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE society_management;
CREATE USER society_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE society_management TO society_user;
\q

# Run schema file
psql -U society_user -d society_management -f backend/schema.sql
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable for database
export DATABASE_URL="postgresql://society_user:your_password@localhost:5432/society_management"

# Initialize database
python init_db.py

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

The application will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Default Login Credentials

After database initialization, use these credentials to login:

- **Username**: admin
- **Password**: admin123

**⚠️ Important**: Change the default password immediately after first login!

## Quick Start Guide

1. **Start PostgreSQL** and create the database
2. **Run backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   export DATABASE_URL="postgresql://society_user:your_password@localhost:5432/society_management"
   python init_db.py
   python main.py
   ```
3. **Run frontend** (in new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```
4. **Access application** at http://localhost:3000
5. **Login** with admin/admin123

## Project Structure

See the complete file structure in the project directory.

## Support

For detailed documentation, API endpoints, deployment guides, and troubleshooting, refer to the full README in the project.
