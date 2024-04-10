from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionForOrder(Base):
    __tablename__ = "promotion_for_order"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    # promotion_id = Column(String,  unique = False, nullable = False)
    # purchase_order_id = Column(String,  unique = False, nullable =False)
    
    promotion_id = Column(String, ForeignKey('promotion.id'), unique = False, nullable = False)
    purchase_order_id = Column(String, ForeignKey('purchase_order.id'), unique = False, nullable =False)
    
    promotion = relationship('Promotion')
    purchase_order = relationship('PurchaseOrder')