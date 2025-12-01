from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ACCOUNTS = "accounts"
    OPERATIONS = "operations"
    FLAT_OWNER = "flat_owner"

class FlatType(str, enum.Enum):
    RESIDENT = "resident"
    TENANT = "tenant"

class VendorStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    PENDING = "pending"
    OVERDUE = "overdue"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone_number = Column(String)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    flat = relationship("Flat", back_populates="owner", uselist=False)

class Flat(Base):
    __tablename__ = "flats"
    
    id = Column(Integer, primary_key=True, index=True)
    flat_number = Column(String, unique=True, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner_name = Column(String, nullable=False)
    owner_email = Column(String, nullable=False)
    owner_phone = Column(String, nullable=False)
    flat_sq_size = Column(Float, nullable=False)
    flat_type = Column(Enum(FlatType), nullable=False, default=FlatType.RESIDENT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="flat")
    tenant_history = relationship("TenantHistory", back_populates="flat", order_by="desc(TenantHistory.agreement_start_date)")
    residents = relationship("FlatResident", back_populates="flat")
    maintenance_records = relationship("Maintenance", back_populates="flat")

class TenantHistory(Base):
    __tablename__ = "tenant_history"
    
    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    tenant_name = Column(String, nullable=False)
    tenant_email = Column(String, nullable=False)
    tenant_phone = Column(String, nullable=False)
    number_of_tenants = Column(Integer, nullable=False)
    tenant_ids = Column(Text)  # JSON string of ID details
    agreement_document = Column(String)  # Path to agreement file
    agreement_duration = Column(Integer)  # in months
    agreement_start_date = Column(DateTime, nullable=False)
    agreement_end_date = Column(DateTime)
    is_current = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    flat = relationship("Flat", back_populates="tenant_history")

class FlatResident(Base):
    __tablename__ = "flat_residents"
    
    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    resident_name = Column(String, nullable=False)
    resident_email = Column(String)
    resident_phone = Column(String)
    relationship_with_owner = Column(String)  # e.g., Family, Self, etc.
    age = Column(Integer)
    id_proof = Column(String)  # Path to ID document
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    flat = relationship("Flat", back_populates="residents")

class Maintenance(Base):
    __tablename__ = "maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    base_amount = Column(Float, nullable=False)
    interest = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime)
    invoice_number = Column(String, unique=True)
    receipt_number = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    flat = relationship("Flat", back_populates="maintenance_records")

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, nullable=False)
    vendor_work = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String)
    business_details = Column(Text)
    status = Column(Enum(VendorStatus), default=VendorStatus.ACTIVE)
    total_charges = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    amount_remaining = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
