-- Society Management System Database Schema
-- PostgreSQL Database Schema

-- Create Database
CREATE DATABASE society_management;

-- Connect to the database
\c society_management;

-- Create ENUM types
CREATE TYPE user_role AS ENUM ('admin', 'accounts', 'operations', 'flat_owner');
CREATE TYPE flat_type AS ENUM ('resident', 'tenant');
CREATE TYPE vendor_status AS ENUM ('active', 'completed', 'on_hold');
CREATE TYPE payment_status AS ENUM ('paid', 'pending', 'overdue');

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    role user_role NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flats Table
CREATE TABLE flats (
    id SERIAL PRIMARY KEY,
    flat_number VARCHAR(50) UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    owner_name VARCHAR(255) NOT NULL,
    owner_email VARCHAR(255) NOT NULL,
    owner_phone VARCHAR(20) NOT NULL,
    flat_sq_size FLOAT NOT NULL,
    flat_type flat_type NOT NULL DEFAULT 'resident',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tenant History Table
CREATE TABLE tenant_history (
    id SERIAL PRIMARY KEY,
    flat_id INTEGER NOT NULL REFERENCES flats(id) ON DELETE CASCADE,
    tenant_name VARCHAR(255) NOT NULL,
    tenant_email VARCHAR(255) NOT NULL,
    tenant_phone VARCHAR(20) NOT NULL,
    number_of_tenants INTEGER NOT NULL,
    tenant_ids TEXT,
    agreement_document VARCHAR(500),
    agreement_duration INTEGER NOT NULL,
    agreement_start_date TIMESTAMP NOT NULL,
    agreement_end_date TIMESTAMP,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flat Residents Table
CREATE TABLE flat_residents (
    id SERIAL PRIMARY KEY,
    flat_id INTEGER NOT NULL REFERENCES flats(id) ON DELETE CASCADE,
    resident_name VARCHAR(255) NOT NULL,
    resident_email VARCHAR(255),
    resident_phone VARCHAR(20),
    relationship_with_owner VARCHAR(100),
    age INTEGER,
    id_proof VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance Table
CREATE TABLE maintenance (
    id SERIAL PRIMARY KEY,
    flat_id INTEGER NOT NULL REFERENCES flats(id) ON DELETE CASCADE,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    year INTEGER NOT NULL,
    base_amount FLOAT NOT NULL,
    interest FLOAT DEFAULT 0.0,
    total_amount FLOAT NOT NULL,
    amount_paid FLOAT DEFAULT 0.0,
    payment_status payment_status DEFAULT 'pending',
    due_date TIMESTAMP NOT NULL,
    paid_date TIMESTAMP,
    invoice_number VARCHAR(100) UNIQUE,
    receipt_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(flat_id, month, year)
);

-- Vendors Table
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    vendor_work VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    business_details TEXT,
    status vendor_status DEFAULT 'active',
    total_charges FLOAT DEFAULT 0.0,
    amount_paid FLOAT DEFAULT 0.0,
    amount_remaining FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_flats_number ON flats(flat_number);
CREATE INDEX idx_flats_owner ON flats(owner_id);
CREATE INDEX idx_tenant_flat ON tenant_history(flat_id);
CREATE INDEX idx_tenant_current ON tenant_history(is_current);
CREATE INDEX idx_resident_flat ON flat_residents(flat_id);
CREATE INDEX idx_maintenance_flat ON maintenance(flat_id);
CREATE INDEX idx_maintenance_status ON maintenance(payment_status);
CREATE INDEX idx_maintenance_month_year ON maintenance(month, year);
CREATE INDEX idx_vendor_status ON vendors(status);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_flats_updated_at BEFORE UPDATE ON flats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tenant_history_updated_at BEFORE UPDATE ON tenant_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_flat_residents_updated_at BEFORE UPDATE ON flat_residents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_maintenance_updated_at BEFORE UPDATE ON maintenance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON vendors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin user (password: admin123)
INSERT INTO users (username, email, hashed_password, full_name, phone_number, role)
VALUES (
    'admin',
    'admin@society.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7xlL3KEUya',
    'System Administrator',
    '1234567890',
    'admin'
);

-- Sample Data (Optional)
-- You can uncomment these to add sample data

-- INSERT INTO users (username, email, hashed_password, full_name, phone_number, role)
-- VALUES 
--     ('accounts', 'accounts@society.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7xlL3KEUya', 'Accounts Manager', '1234567891', 'accounts'),
--     ('operations', 'operations@society.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7xlL3KEUya', 'Operations Manager', '1234567892', 'operations');
