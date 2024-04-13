from sqlalchemy import ARRAY, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

class InvoiceForCustomer(Base):
    __tablename__ = "invoice_for_customer"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    total = Column(Integer, unique = False, nullable = False)
    status = Column(String, unique = False, nullable = False)
    payment_method = Column(String, unique = False, nullable = False)
    
    belong_to_order = Column(String, ForeignKey('purchase_order.id'), unique = True, nullable = False)
    order_detail = Column(ARRAY(Integer), unique = True, nullable = False)
    # detail_order = Column(ARRAY(Integer), ForeignKey('order.id'), unique = True, nullable = False)
    purchase_order = relationship('PurchaseOrder')    
    # order = relationship('OrderDetail',uselist=True)
   

