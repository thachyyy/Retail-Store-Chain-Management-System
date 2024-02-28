from sqlalchemy import Column, ForeignKey, Integer, Float, Date
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Batch(Base):
    __tablename__ = "batch"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    quantity = Column(Integer, unique = False, nullable = False)
    import_price = Column(Float, unique = False, nullable = False)
    manufacturing_date = Column(Date, unique = False, nullable = True)
    expiry_date = Column(Date, unique = False, nullable = True)
    # belong_to_branch = Column(UUID(as_uuid=True),   unique = False, nullable = False)
    # belong_to_receipt = Column(UUID(as_uuid=True),  unique = False, nullable = False)
    
    
    belong_to_branch = Column(UUID(as_uuid=True), ForeignKey('branch.id'), unique = False, nullable = False)
    belong_to_receipt = Column(UUID(as_uuid=True), ForeignKey ('warehouse_receipts.id'), unique = False, nullable = False)
    
    branch = relationship('Branch')
    warehouse_receipt = relationship('warehouse_receipt')