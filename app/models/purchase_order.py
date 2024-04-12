from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    estimated_delivery_date = Column(DateTime, unique = False, nullable = False)
    subtotal = Column(Integer, unique = False, nullable = False)
    total = Column(Integer, unique = False, nullable = False)
    tax_percentage = Column(Integer, unique = False, nullable = False)
    tax = Column(Integer, unique = False, nullable = True)
    promote = Column(Integer, unique = False, nullable = True)
    status = Column(String, unique = False, nullable = True)
    note = Column(String, unique = False, nullable = True)
    # handle_by = Column(String,  unique = False, nullable = False)
    # belong_to_customer = Column(String,  unique = False, nullable = False)
    
    batch = relationship("OrderDetail", back_populates="purchase_order")
    handle_by = Column(String, ForeignKey('employee.id'), unique = False, nullable = False)
    belong_to_customer = Column(String, ForeignKey('customer.id'), unique = False, nullable = True)
    
    employee = relationship('Employee')
    customer = relationship('Customer')