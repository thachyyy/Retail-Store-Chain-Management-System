from sqlalchemy import Column, Integer, ForeignKey, String, DateTime,Date
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base

class ContractForVendor(Base):
    __tablename__ = 'contract_for_vendor'

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    start_date = Column(DateTime, unique = False, nullable = False)
    end_date = Column(DateTime, unique = False, nullable = False)
    tenant_id = Column(String, unique=False, nullable=False)
    belong_to_vendor = Column(String(255), unique = False, nullable = False)
    minimum_order_amount = Column(Integer, unique = False, nullable = True)
    minimum_order_quantity = Column(Integer, unique = False, nullable = True)
    ordering_cycle_amount = Column(Integer, unique = False, nullable = True)
    ordering_cycle_quantity = Column(Integer, unique = False, nullable = True)
    branch = Column(String,unique = False,nullable = True)
    latest_import = Column(Date, nullable = True)
    next_import = Column(Date, nullable = True)
    period = Column(Integer, nullable = True)
    pdf_url = Column(String, nullable = True)
    
    # vendor = relationship('Vendor')