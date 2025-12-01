from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from models import UserRole, FlatType, VendorStatus, PaymentStatus

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Flat Schemas
class FlatBase(BaseModel):
    flat_number: str
    owner_name: str
    owner_email: EmailStr
    owner_phone: str
    flat_sq_size: float
    flat_type: FlatType

class FlatCreate(FlatBase):
    owner_id: int

class FlatUpdate(BaseModel):
    owner_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    owner_phone: Optional[str] = None
    flat_sq_size: Optional[float] = None
    flat_type: Optional[FlatType] = None

class FlatResponse(FlatBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Tenant History Schemas
class TenantHistoryBase(BaseModel):
    tenant_name: str
    tenant_email: EmailStr
    tenant_phone: str
    number_of_tenants: int
    tenant_ids: Optional[str] = None
    agreement_duration: int
    agreement_start_date: datetime

class TenantHistoryCreate(TenantHistoryBase):
    flat_id: int
    agreement_document: Optional[str] = None

class TenantHistoryUpdate(BaseModel):
    tenant_name: Optional[str] = None
    tenant_email: Optional[EmailStr] = None
    tenant_phone: Optional[str] = None
    number_of_tenants: Optional[int] = None
    is_current: Optional[bool] = None

class TenantHistoryResponse(TenantHistoryBase):
    id: int
    flat_id: int
    agreement_end_date: Optional[datetime] = None
    is_current: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Flat Resident Schemas
class FlatResidentBase(BaseModel):
    resident_name: str
    resident_email: Optional[EmailStr] = None
    resident_phone: Optional[str] = None
    relationship_with_owner: Optional[str] = None
    age: Optional[int] = None

class FlatResidentCreate(FlatResidentBase):
    flat_id: int
    id_proof: Optional[str] = None

class FlatResidentUpdate(BaseModel):
    resident_name: Optional[str] = None
    resident_email: Optional[EmailStr] = None
    resident_phone: Optional[str] = None
    relationship_with_owner: Optional[str] = None
    age: Optional[int] = None

class FlatResidentResponse(FlatResidentBase):
    id: int
    flat_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Maintenance Schemas
class MaintenanceBase(BaseModel):
    base_amount: float
    month: int
    year: int

class MaintenanceCreate(MaintenanceBase):
    flat_id: int

class MaintenanceUpdate(BaseModel):
    payment_status: Optional[PaymentStatus] = None
    amount_paid: Optional[float] = None

class MaintenanceResponse(MaintenanceBase):
    id: int
    flat_id: int
    interest: float
    total_amount: float
    amount_paid: float
    payment_status: PaymentStatus
    due_date: datetime
    paid_date: Optional[datetime] = None
    invoice_number: Optional[str] = None
    receipt_number: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Vendor Schemas
class VendorBase(BaseModel):
    vendor_name: str
    vendor_work: str
    phone_number: str
    email: Optional[EmailStr] = None
    business_details: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    vendor_work: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    business_details: Optional[str] = None
    status: Optional[VendorStatus] = None
    total_charges: Optional[float] = None
    amount_paid: Optional[float] = None

class VendorResponse(VendorBase):
    id: int
    status: VendorStatus
    total_charges: float
    amount_paid: float
    amount_remaining: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
