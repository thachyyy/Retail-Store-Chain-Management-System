from sqlalchemy import Column, String, Date, Boolean,  ForeignKey, Integer
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class WarehouseReceipt(Base):
    __tablename__ = "warehouse_receipt"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    is_contract = Column(Boolean, unique = False, nullable = False)
    estimated_date = Column(Date, unique = False, nullable = False)
    delivery_status = Column(String, unique = False, nullable = False)
    payment_status = Column(String, unique = False, nullable = False)
    subtotal = Column(Integer, unique = False, nullable = False)
    promotion = Column(Integer, unique = False, nullable = True)
    total = Column(Integer, unique = False, nullable = False)
    # created_by = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # belong_to_vendor = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # belong_to_contract = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # belong_to_invoice = Column(UUID(as_uuid=True), unique = False, nullable = True)
    
    created_by = Column(UUID(as_uuid=True), ForeignKey('employee.id'), unique = False, nullable = False)
    belong_to_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'), unique = False, nullable = False)
    belong_to_contract = Column(UUID(as_uuid=True), ForeignKey('contract.id'), unique = False, nullable = False)
    belong_to_invoice = Column(UUID(as_uuid=True), ForeignKey('invoice_from_vendor.id'), unique = False, nullable = True)
    
    employee = relationship('Employee')
    vendor = relationship('Vendor')
    contract = relationship('Contract')
    invoice_from_vendor = relationship('InvoiceFromVendor')