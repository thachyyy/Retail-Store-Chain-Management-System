from sqlalchemy import Column, Integer,  Date, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Batch(Base):
    __tablename__ = "batch"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    quantity = Column(Integer, nullable = False)
    import_price = Column(Integer, nullable = False)
    manufacturing_date = Column(Date, nullable = True)
    expiry_date = Column(Date, nullable = True)
    # belong_to_branch = Column(UUID(as_uuid=True), nullable = False)
    # belong_to_receipt = Column(UUID(as_uuid=True),  nullable = False)
    product_id = Column(String, ForeignKey('product.id'), nullable=False)
    
    purchase_order = relationship("OrderDetail", back_populates="batch")
    product_id = Column(String, ForeignKey('product.id'), unique = False, nullable = False)
    belong_to_branch = Column(String, ForeignKey('branch.id'), unique = False, nullable = False)
    belong_to_receipt = Column(String, ForeignKey('import_order.id'), unique = False, nullable = True)
    tenant_id = Column(String, unique=False, nullable=False)
    
    product = relationship('Product')
    branch = relationship('Branch')
    import_order = relationship('ImportOrder')
    product = relationship('Product')