from sqlalchemy import Column, String,  DateTime, Date, ForeignKey, Integer
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class InvoiceFromVendor(Base):
    __tablename__ = "invoice_from_vendor"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, unique = False, nullable = False)
    payment_deadline = Column(Date, unique = False, nullable = False)
    total = Column(Integer, unique = False, nullable = False)
    status = Column(String, unique = False, nullable = False)
    vendor_id = Column(String, ForeignKey('vendor.id'), unique = False, nullable = False)
    
    vendor = relationship('Vendor')