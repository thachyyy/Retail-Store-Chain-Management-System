from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

'''
    "Đang hợp tác",
    "Dừng hợp tác"
'''

class Vendor(Base):
    __tablename__ = "vendor"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    company_name = Column(String(255), unique=False, nullable=False)
    vendor_name = Column(String(255), unique=False, nullable=False)
    phone_number = Column(String(255), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    address = Column(String(255), unique=False, nullable=True)
    district = Column(String(64), unique=False, nullable=True)
    province = Column(String(64), unique=False, nullable=True)
    status = Column(String(64), unique=False, nullable=False, default = 'Đang hợp tác')
    note = Column(String, unique=False, nullable=True)