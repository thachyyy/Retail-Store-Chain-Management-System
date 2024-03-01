from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Vendor(Base):
    __tablename__ = "vendor"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    company_name = Column(String(255), unique=False, nullable=True)
    vendor_name = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    address = Column(String(255), unique=False, nullable=False)
    district = Column(String(64), unique=False, nullable=True)
    province = Column(String(64), unique=False, nullable=True)
    status = Column(String(64), unique=False, nullable=True)
    note = Column(String, unique=False, nullable=True)
    