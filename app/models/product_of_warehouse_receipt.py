from sqlalchemy import Column, ForeignKey, Integer
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ProductOfWarehouseReceipt(Base):
    __tablename__ = "product_of_warehouse_receipt"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    import_price = Column(Integer, unique = False, nullable = False)
    # product_id = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # warehouse_receipt_id = Column(UUID(as_uuid=True),  unique = False, nullable = False)
   
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), unique = False, nullable = False)
    warehouse_receipt_id = Column(UUID(as_uuid=True), ForeignKey('warehouse_receipt.id'), unique = False, nullable = False)
    
    product = relationship('Product')
    warehouse_receipt = relationship('WarehouseReceipt')     