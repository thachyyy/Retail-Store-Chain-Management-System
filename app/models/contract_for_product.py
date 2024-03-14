from sqlalchemy import Column, Integer, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ContractForProduct(Base):
    __tablename__ = "contract_for_product"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    
    price = Column(Integer, unique = False, nullable = False)
    # contract_id = Column(UUID(as_uuid=True), unique = False, nullable = False)
    # product_id = Column(UUID(as_uuid=True), unique = False, nullable = False)
    
    contract_for_vendor_id = Column(UUID(as_uuid=True), ForeignKey('contract_for_vendor.id'), unique = False, nullable = False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), unique = False, nullable = False)
    contract_for_vendor = relationship('ContractForVendor')
    product = relationship('Product')