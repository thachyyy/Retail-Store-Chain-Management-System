from sqlalchemy import Column,  Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base

class ContractForVendor(Base):
    __tablename__ = 'contract_for_vendor'

    id = Column(UUID(as_uuid=True), primary_key=True)
    start_date = Column(DateTime, unique = False, nullable = False)
    end_date = Column(DateTime, unique = False, nullable = False)
    minimum_order_amount = Column(Integer, unique = False, nullable = True)
    minimum_order_quantity = Column(Integer, unique = False, nullable = True)
    ordering_cycle_amount = Column(Integer, unique = False, nullable = True)
    ordering_cycle_quantity = Column(Integer, unique = False, nullable = True)
    # belong_to_vendor = Column(String(255), unique = False, nullable = False)

    belong_to_vendor = Column(String(255), ForeignKey('vendor.vendor_name'), unique = False, nullable = False)
    
    vendor = relationship('Vendor')