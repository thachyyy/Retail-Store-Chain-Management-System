from sqlalchemy import Column, Integer,  Date, ForeignKey, String
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Batch(Base):
    __tablename__ = "batch"
    
    id = Column(String, primary_key=True)
    quantity = Column(Integer, nullable = False)
    import_price = Column(Integer, nullable = False)
    manufacturing_date = Column(Date, nullable = True)
    expiry_date = Column(Date, nullable = True)
    # belong_to_branch = Column(UUID(as_uuid=True), nullable = False)
    # belong_to_receipt = Column(UUID(as_uuid=True),  nullable = False)
    
    belong_to_branch = Column(String, ForeignKey('branch.id'), unique = False, nullable = False)
    belong_to_receipt = Column(String, ForeignKey('import_order.id'), unique = False, nullable = False)
    
    branch = relationship('Branch')
    import_order = relationship('ImportOrder')