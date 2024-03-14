from sqlalchemy import Column, ForeignKey, Integer
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ProductOfImportOrder(Base):
    __tablename__ = "product_of_import_order"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    import_price = Column(Integer, unique = False, nullable = False)
    # product_id = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # import_order_id = Column(UUID(as_uuid=True),  unique = False, nullable = False)
   
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), unique = False, nullable = False)
    import_order_id = Column(UUID(as_uuid=True), ForeignKey('import_order.id'), unique = False, nullable = False)
    
    product = relationship('Product')
    import_order = relationship('ImportOrder')     