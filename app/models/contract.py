from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base

class Contract(Base):
    __tablename__ = 'contract'

    id = Column(UUID(as_uuid=True), primary_key=True)
    start_date = Column(DateTime, unique = False, nullable = False)
    end_date = Column(DateTime, unique = False, nulllable = False)
    minimum_order_amount = Column(Float, unique = False, nullable = True)
    minimum_order_quantity = Column(Integer, unique = False, nullable = True)
    ordering_cycle_amount = Column(Integer, unique = False, nullable = True)
    ordering_cycle_quantity = Column(Integer, unique = False, nullable = True)
    belong_to_vendor = Column(UUID(as_uuid=True), ForeignKey = ('vendor.id'), unique = False, nullable = False)
    
    vendor = relationship('Vendor')