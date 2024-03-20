from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, unique = False, nullable = False)
    estimated_delivery_date = Column(DateTime, unique = False, nullable = False)
    tax = Column(Integer, unique = False, nullable = True)
    subtotal = Column(Integer, unique = False, nullable = False)
    promote = Column(Integer, unique = False, nullable = True)
    total = Column(Integer, unique = False, nullable = False)
    tax_percentage = Column(Integer, unique = False, nullable = False)
    status = Column(String, unique = False, nullable = True)
    note = Column(String, unique = False, nullable = True)
    # handle_by = Column(String,  unique = False, nullable = False)
    # belong_to_customer = Column(String,  unique = False, nullable = False)
    
    
    handle_by = Column(String, ForeignKey('employee.id'), unique = False, nullable = False)
    belong_to_customer = Column(String, ForeignKey('customer.id'), unique = False, nullable = True)
    
    employee = relationship('Employee')
    customer = relationship('Customer')