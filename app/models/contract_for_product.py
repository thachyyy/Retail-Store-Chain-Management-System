from sqlalchemy import Column, Float
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ContractForProduct(Base):
    __tablename__ = "contract_for_product"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey = ('contract.id'), unique = False, nullable = False)
    product_id = Column(UUID(as_uuid=True), ForeignKey = ('product.id'), unique = False, nullable = False)
    price = Column(Float, unique = False, nullable = False)
    
    contract = relationship('Contract')
    product = relationship('Product')