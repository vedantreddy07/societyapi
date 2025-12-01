from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
import schemas
from auth import get_password_hash
from datetime import datetime, timedelta
from typing import List, Optional

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Flat CRUD
def get_flat(db: Session, flat_id: int):
    return db.query(models.Flat).filter(models.Flat.id == flat_id).first()

def get_flat_by_number(db: Session, flat_number: str):
    return db.query(models.Flat).filter(models.Flat.flat_number == flat_number).first()

def get_flats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flat).offset(skip).limit(limit).all()

def create_flat(db: Session, flat: schemas.FlatCreate):
    db_flat = models.Flat(**flat.dict())
    db.add(db_flat)
    db.commit()
    db.refresh(db_flat)
    return db_flat

def update_flat(db: Session, flat_id: int, flat: schemas.FlatUpdate):
    db_flat = get_flat(db, flat_id)
    if db_flat:
        for key, value in flat.dict(exclude_unset=True).items():
            setattr(db_flat, key, value)
        db_flat.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_flat)
    return db_flat

def delete_flat(db: Session, flat_id: int):
    db_flat = get_flat(db, flat_id)
    if db_flat:
        db.delete(db_flat)
        db.commit()
    return db_flat

# Tenant History CRUD
def get_tenant_history(db: Session, tenant_id: int):
    return db.query(models.TenantHistory).filter(models.TenantHistory.id == tenant_id).first()

def get_tenant_histories_by_flat(db: Session, flat_id: int):
    return db.query(models.TenantHistory).filter(
        models.TenantHistory.flat_id == flat_id
    ).order_by(models.TenantHistory.agreement_start_date.desc()).all()

def get_current_tenant(db: Session, flat_id: int):
    return db.query(models.TenantHistory).filter(
        and_(models.TenantHistory.flat_id == flat_id, models.TenantHistory.is_current == True)
    ).first()

def create_tenant_history(db: Session, tenant: schemas.TenantHistoryCreate):
    # Mark all previous tenants as not current
    db.query(models.TenantHistory).filter(
        models.TenantHistory.flat_id == tenant.flat_id
    ).update({"is_current": False})
    
    # Calculate end date
    end_date = tenant.agreement_start_date + timedelta(days=30 * tenant.agreement_duration)
    
    db_tenant = models.TenantHistory(
        **tenant.dict(),
        agreement_end_date=end_date,
        is_current=True
    )
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

def update_tenant_history(db: Session, tenant_id: int, tenant: schemas.TenantHistoryUpdate):
    db_tenant = get_tenant_history(db, tenant_id)
    if db_tenant:
        for key, value in tenant.dict(exclude_unset=True).items():
            setattr(db_tenant, key, value)
        db_tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_tenant)
    return db_tenant

def delete_tenant_history(db: Session, tenant_id: int):
    db_tenant = get_tenant_history(db, tenant_id)
    if db_tenant:
        db.delete(db_tenant)
        db.commit()
    return db_tenant

# Flat Resident CRUD
def get_flat_resident(db: Session, resident_id: int):
    return db.query(models.FlatResident).filter(models.FlatResident.id == resident_id).first()

def get_flat_residents_by_flat(db: Session, flat_id: int):
    return db.query(models.FlatResident).filter(models.FlatResident.flat_id == flat_id).all()

def create_flat_resident(db: Session, resident: schemas.FlatResidentCreate):
    db_resident = models.FlatResident(**resident.dict())
    db.add(db_resident)
    db.commit()
    db.refresh(db_resident)
    return db_resident

def update_flat_resident(db: Session, resident_id: int, resident: schemas.FlatResidentUpdate):
    db_resident = get_flat_resident(db, resident_id)
    if db_resident:
        for key, value in resident.dict(exclude_unset=True).items():
            setattr(db_resident, key, value)
        db_resident.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_resident)
    return db_resident

def delete_flat_resident(db: Session, resident_id: int):
    db_resident = get_flat_resident(db, resident_id)
    if db_resident:
        db.delete(db_resident)
        db.commit()
    return db_resident

# Maintenance CRUD
def get_maintenance(db: Session, maintenance_id: int):
    return db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()

def get_maintenance_by_flat(db: Session, flat_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Maintenance).filter(
        models.Maintenance.flat_id == flat_id
    ).order_by(models.Maintenance.year.desc(), models.Maintenance.month.desc()).offset(skip).limit(limit).all()

def get_maintenance_by_month_year(db: Session, month: int, year: int):
    return db.query(models.Maintenance).filter(
        and_(models.Maintenance.month == month, models.Maintenance.year == year)
    ).all()

def create_maintenance(db: Session, maintenance: schemas.MaintenanceCreate):
    # Generate invoice number
    invoice_number = f"INV-{maintenance.flat_id}-{maintenance.year}{maintenance.month:02d}"
    
    # Calculate due date (10th of the month)
    due_date = datetime(maintenance.year, maintenance.month, 10)
    
    db_maintenance = models.Maintenance(
        **maintenance.dict(),
        total_amount=maintenance.base_amount,
        invoice_number=invoice_number,
        due_date=due_date
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

def update_maintenance(db: Session, maintenance_id: int, maintenance: schemas.MaintenanceUpdate):
    db_maintenance = get_maintenance(db, maintenance_id)
    if db_maintenance:
        for key, value in maintenance.dict(exclude_unset=True).items():
            setattr(db_maintenance, key, value)
        
        # Generate receipt if paid
        if maintenance.payment_status == models.PaymentStatus.PAID and not db_maintenance.receipt_number:
            db_maintenance.receipt_number = f"REC-{db_maintenance.flat_id}-{db_maintenance.year}{db_maintenance.month:02d}"
            db_maintenance.paid_date = datetime.utcnow()
        
        db_maintenance.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_maintenance)
    return db_maintenance

def apply_interest_to_overdue(db: Session):
    """Apply 10% interest to overdue maintenance"""
    current_date = datetime.utcnow()
    overdue_records = db.query(models.Maintenance).filter(
        and_(
            models.Maintenance.payment_status == models.PaymentStatus.PENDING,
            models.Maintenance.due_date < current_date
        )
    ).all()
    
    for record in overdue_records:
        record.interest = record.base_amount * 0.10
        record.total_amount = record.base_amount + record.interest
        record.payment_status = models.PaymentStatus.OVERDUE
    
    db.commit()
    return len(overdue_records)

# Vendor CRUD
def get_vendor(db: Session, vendor_id: int):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).offset(skip).limit(limit).all()

def get_vendors_by_status(db: Session, status: models.VendorStatus):
    return db.query(models.Vendor).filter(models.Vendor.status == status).all()

def create_vendor(db: Session, vendor: schemas.VendorCreate):
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def update_vendor(db: Session, vendor_id: int, vendor: schemas.VendorUpdate):
    db_vendor = get_vendor(db, vendor_id)
    if db_vendor:
        for key, value in vendor.dict(exclude_unset=True).items():
            setattr(db_vendor, key, value)
        
        # Calculate remaining amount
        if vendor.total_charges is not None or vendor.amount_paid is not None:
            db_vendor.amount_remaining = db_vendor.total_charges - db_vendor.amount_paid
        
        db_vendor.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int):
    db_vendor = get_vendor(db, vendor_id)
    if db_vendor:
        db.delete(db_vendor)
        db.commit()
    return db_vendor
