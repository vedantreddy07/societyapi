# API Documentation

Complete API reference for Society Management System. For interactive documentation, visit `/docs` when the server is running.

## Base URL
- Development: `http://localhost:8000`
- Production: Your deployed URL

## Authentication

JWT Bearer token authentication is used. Include the token in request headers:
```
Authorization: Bearer <your_token>
```

### POST /auth/login
Login and receive access token.

**Request (form-data):**
- username: string
- password: string

**Response:**
```json
{
  "access_token": "token_here",
  "token_type": "bearer"
}
```

### GET /auth/me
Get current authenticated user details.

## Users API

### GET /users/
List all users (Admin, Operations only)

### POST /users/
Create new user (Admin only)

### GET /users/{id}
Get user by ID

### PUT /users/{id}
Update user (Admin only)

### DELETE /users/{id}
Delete user (Admin only)

## Flats API

### GET /flats/
List all flats

### POST /flats/
Create new flat (Admin, Operations)

### GET /flats/{id}
Get flat details

### PUT /flats/{id}
Update flat (Admin, Operations)

### DELETE /flats/{id}
Delete flat (Admin)

## Tenants API

### GET /tenants/flat/{flat_id}
Get tenant history for a flat

### POST /tenants/
Create tenant record (Admin, Operations)

### PUT /tenants/{id}
Update tenant

### DELETE /tenants/{id}
Delete tenant (Admin)

## Residents API

### GET /residents/flat/{flat_id}
Get residents for a flat

### POST /residents/
Create resident

### PUT /residents/{id}
Update resident

### DELETE /residents/{id}
Delete resident

## Maintenance API

### GET /maintenance/flat/{flat_id}
Get maintenance records for a flat

### POST /maintenance/
Create maintenance record (Admin, Accounts)

### PUT /maintenance/{id}
Update maintenance (Admin, Accounts)

### POST /maintenance/apply-interest
Apply 10% interest to overdue records (Admin, Accounts)

## Vendors API

### GET /vendors/
List all vendors

### POST /vendors/
Create vendor (Admin, Operations)

### GET /vendors/{id}
Get vendor details

### PUT /vendors/{id}
Update vendor

### DELETE /vendors/{id}
Delete vendor (Admin)

For detailed request/response schemas, visit the interactive Swagger documentation at `/docs`.
