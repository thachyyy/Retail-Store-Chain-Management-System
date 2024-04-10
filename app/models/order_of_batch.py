from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class OrderOfBatch(Base):
    __tablename__ = "order_of_batch"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    price = Column(Integer, unique = False, nullable = False)
    quantity = Column(Integer, unique = False, nullable = False)
    # purchase_order_id = Column(String, unique = False, nullable = False)
    # batch_id = Column(String, unique = False, nullable = False)
    
    purchase_order_id = Column(String, ForeignKey('purchase_order.id'), unique = False, nullable = False)
    batch_id = Column(String, ForeignKey('batch.id'), unique = False, nullable = False)
    
    batch = relationship('Batch')
    purchase_order = relationship('PurchaseOrder')