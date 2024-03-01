from sqlalchemy import Column, Float, Integer, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class OrderOfBatch(Base):
    __tablename__ = "order_of_batch"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    purchase_order_id = Column(UUID(as_uuid=True), ForeignKey('purchase_order.id'), unique = False, nullable = False)
    batch_id = Column(UUID(as_uuid=True), ForeignKey('batch.id'), unique = False, nullable = False)
    price = Column(Float, unique = False, nullable = False)
    quantity = Column(Integer, unique = False, nullable = False)
    
    batch = relationship('Batch')
    purchase_order = relationship('PurchaseOrder')