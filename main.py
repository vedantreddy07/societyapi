from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import models
import schemas
import crud
import auth
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Society Management API",
    description="API for managing society operations including residents, maintenance, and vendors",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Routes
@app.post("/auth/login", response_model=schemas.Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login to get access token"""
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserResponse, tags=["Authentication"])
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """Get current user details"""
    return current_user

# User Routes
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Create a new user (Admin only)"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.UserResponse], tags=["Users"])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Get all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user by ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Update user (Admin only)"""
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Delete user (Admin only)"""
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Flat Routes
@app.post("/flats/", response_model=schemas.FlatResponse, tags=["Flats"], status_code=status.HTTP_201_CREATED)
async def create_flat(
    flat: schemas.FlatCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Create a new flat"""
    db_flat = crud.get_flat_by_number(db, flat_number=flat.flat_number)
    if db_flat:
        raise HTTPException(status_code=400, detail="Flat number already exists")
    return crud.create_flat(db=db, flat=flat)

@app.get("/flats/", response_model=List[schemas.FlatResponse], tags=["Flats"])
async def read_flats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all flats"""
    flats = crud.get_flats(db, skip=skip, limit=limit)
    return flats

@app.get("/flats/{flat_id}", response_model=schemas.FlatResponse, tags=["Flats"])
async def read_flat(
    flat_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get flat by ID"""
    db_flat = crud.get_flat(db, flat_id=flat_id)
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    return db_flat

@app.put("/flats/{flat_id}", response_model=schemas.FlatResponse, tags=["Flats"])
async def update_flat(
    flat_id: int,
    flat: schemas.FlatUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Update flat"""
    db_flat = crud.update_flat(db, flat_id=flat_id, flat=flat)
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    return db_flat

@app.delete("/flats/{flat_id}", tags=["Flats"])
async def delete_flat(
    flat_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Delete flat (Admin only)"""
    db_flat = crud.delete_flat(db, flat_id=flat_id)
    if db_flat is None:
        raise HTTPException(status_code=404, detail="Flat not found")
    return {"message": "Flat deleted successfully"}

# Tenant History Routes
@app.post("/tenants/", response_model=schemas.TenantHistoryResponse, tags=["Tenants"], status_code=status.HTTP_201_CREATED)
async def create_tenant_history(
    tenant: schemas.TenantHistoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Create tenant history record"""
    return crud.create_tenant_history(db=db, tenant=tenant)

@app.get("/tenants/flat/{flat_id}", response_model=List[schemas.TenantHistoryResponse], tags=["Tenants"])
async def read_tenant_histories(
    flat_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all tenant histories for a flat"""
    return crud.get_tenant_histories_by_flat(db, flat_id=flat_id)

@app.get("/tenants/{tenant_id}", response_model=schemas.TenantHistoryResponse, tags=["Tenants"])
async def read_tenant_history(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get tenant history by ID"""
    db_tenant = crud.get_tenant_history(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant history not found")
    return db_tenant

@app.put("/tenants/{tenant_id}", response_model=schemas.TenantHistoryResponse, tags=["Tenants"])
async def update_tenant_history(
    tenant_id: int,
    tenant: schemas.TenantHistoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Update tenant history"""
    db_tenant = crud.update_tenant_history(db, tenant_id=tenant_id, tenant=tenant)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant history not found")
    return db_tenant

@app.delete("/tenants/{tenant_id}", tags=["Tenants"])
async def delete_tenant_history(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Delete tenant history (Admin only)"""
    db_tenant = crud.delete_tenant_history(db, tenant_id=tenant_id)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant history not found")
    return {"message": "Tenant history deleted successfully"}

# Flat Residents Routes
@app.post("/residents/", response_model=schemas.FlatResidentResponse, tags=["Residents"], status_code=status.HTTP_201_CREATED)
async def create_flat_resident(
    resident: schemas.FlatResidentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS, models.UserRole.FLAT_OWNER]))
):
    """Create flat resident"""
    return crud.create_flat_resident(db=db, resident=resident)

@app.get("/residents/flat/{flat_id}", response_model=List[schemas.FlatResidentResponse], tags=["Residents"])
async def read_flat_residents(
    flat_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all residents for a flat"""
    return crud.get_flat_residents_by_flat(db, flat_id=flat_id)

@app.get("/residents/{resident_id}", response_model=schemas.FlatResidentResponse, tags=["Residents"])
async def read_flat_resident(
    resident_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get resident by ID"""
    db_resident = crud.get_flat_resident(db, resident_id=resident_id)
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return db_resident

@app.put("/residents/{resident_id}", response_model=schemas.FlatResidentResponse, tags=["Residents"])
async def update_flat_resident(
    resident_id: int,
    resident: schemas.FlatResidentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS, models.UserRole.FLAT_OWNER]))
):
    """Update resident"""
    db_resident = crud.update_flat_resident(db, resident_id=resident_id, resident=resident)
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return db_resident

@app.delete("/residents/{resident_id}", tags=["Residents"])
async def delete_flat_resident(
    resident_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Delete resident"""
    db_resident = crud.delete_flat_resident(db, resident_id=resident_id)
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return {"message": "Resident deleted successfully"}

# Maintenance Routes
@app.post("/maintenance/", response_model=schemas.MaintenanceResponse, tags=["Maintenance"], status_code=status.HTTP_201_CREATED)
async def create_maintenance(
    maintenance: schemas.MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.ACCOUNTS]))
):
    """Create maintenance record"""
    return crud.create_maintenance(db=db, maintenance=maintenance)

@app.get("/maintenance/flat/{flat_id}", response_model=List[schemas.MaintenanceResponse], tags=["Maintenance"])
async def read_maintenance_by_flat(
    flat_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get maintenance records for a flat"""
    return crud.get_maintenance_by_flat(db, flat_id=flat_id, skip=skip, limit=limit)

@app.get("/maintenance/{maintenance_id}", response_model=schemas.MaintenanceResponse, tags=["Maintenance"])
async def read_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get maintenance by ID"""
    db_maintenance = crud.get_maintenance(db, maintenance_id=maintenance_id)
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return db_maintenance

@app.put("/maintenance/{maintenance_id}", response_model=schemas.MaintenanceResponse, tags=["Maintenance"])
async def update_maintenance(
    maintenance_id: int,
    maintenance: schemas.MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.ACCOUNTS]))
):
    """Update maintenance record"""
    db_maintenance = crud.update_maintenance(db, maintenance_id=maintenance_id, maintenance=maintenance)
    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return db_maintenance

@app.post("/maintenance/apply-interest", tags=["Maintenance"])
async def apply_interest(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.ACCOUNTS]))
):
    """Apply 10% interest to all overdue maintenance"""
    count = crud.apply_interest_to_overdue(db)
    return {"message": f"Interest applied to {count} overdue records"}

# Vendor Routes
@app.post("/vendors/", response_model=schemas.VendorResponse, tags=["Vendors"], status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor: schemas.VendorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS]))
):
    """Create a new vendor"""
    return crud.create_vendor(db=db, vendor=vendor)

@app.get("/vendors/", response_model=List[schemas.VendorResponse], tags=["Vendors"])
async def read_vendors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get all vendors"""
    vendors = crud.get_vendors(db, skip=skip, limit=limit)
    return vendors

@app.get("/vendors/{vendor_id}", response_model=schemas.VendorResponse, tags=["Vendors"])
async def read_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get vendor by ID"""
    db_vendor = crud.get_vendor(db, vendor_id=vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@app.put("/vendors/{vendor_id}", response_model=schemas.VendorResponse, tags=["Vendors"])
async def update_vendor(
    vendor_id: int,
    vendor: schemas.VendorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN, models.UserRole.OPERATIONS, models.UserRole.ACCOUNTS]))
):
    """Update vendor"""
    db_vendor = crud.update_vendor(db, vendor_id=vendor_id, vendor=vendor)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@app.delete("/vendors/{vendor_id}", tags=["Vendors"])
async def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.check_role([models.UserRole.ADMIN]))
):
    """Delete vendor (Admin only)"""
    db_vendor = crud.delete_vendor(db, vendor_id=vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {"message": "Society Management API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
