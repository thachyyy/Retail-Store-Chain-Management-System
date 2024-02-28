from sqlalchemy import Column, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class PromotionForOrder(Base):
    __tablename__ = "promotion_for_order"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    # promotion_id = Column(UUID(as_uuid=True),  unique = False, nullable = False)
    # purchase_order_id = Column(UUID(as_uuid=True), unique = False, nullable =False)
    
    promotion_id = Column(UUID(as_uuid=True), ForeignKey('promotion.id'), unique = False, nullable = False)
    purchase_order_id = Column(UUID(as_uuid=True), ForeignKey('purchase_order.id'), unique = False, nullable =False)
    
    promotion = relationship('Promotion')
    purchase_order = relationship('PurchaseOrder')