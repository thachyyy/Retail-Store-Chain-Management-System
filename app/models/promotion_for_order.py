from sqlalchemy import Column, ForeignKey, String
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionForOrder(Base):
    __tablename__ = "promotion_for_order"
    
    id = Column(String, primary_key=True)
    # promotion_id = Column(String,  unique = False, nullable = False)
    # purchase_order_id = Column(String,  unique = False, nullable =False)
    
    promotion_id = Column(String, ForeignKey('promotion.id'), unique = False, nullable = False)
    purchase_order_id = Column(String, ForeignKey('purchase_order.id'), unique = False, nullable =False)
    
    promotion = relationship('Promotion')
    purchase_order = relationship('PurchaseOrder')