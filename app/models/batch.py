from sqlalchemy import Column, Integer,  Date, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Batch(Base):
    __tablename__ = "batch"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    quantity = Column(Integer, nullable = False)
    import_price = Column(Integer, nullable = False)
    manufacturing_date = Column(Date, nullable = True)
    expiry_date = Column(Date, nullable = True)
    # belong_to_branch = Column(UUID(as_uuid=True), nullable = False)
    # belong_to_receipt = Column(UUID(as_uuid=True),  nullable = False)
    
    belong_to_branch = Column(UUID(as_uuid=True), ForeignKey('branch.id'), unique = False, nullable = False)
    belong_to_receipt = Column(UUID(as_uuid=True), ForeignKey('warehouse_receipt.id'), unique = False, nullable = False)
    
    branch = relationship('Branch')
    warehouse_receipt = relationship('WarehouseReceipt')