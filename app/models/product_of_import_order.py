from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ProductOfImportOrder(Base):
    __tablename__ = "product_of_import_order"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    import_price = Column(Integer, unique = False, nullable = False)
    # product_id = Column(String, unique = False, nullable = False)
    # import_order_id = Column(String,  unique = False, nullable = False)
   
    product_id = Column(String, ForeignKey('product.id'), unique = False, nullable = False)
    import_order_id = Column(String, ForeignKey('import_order.id'), unique = False, nullable = False)
    
    product = relationship('Product')
    import_order = relationship('ImportOrder')     