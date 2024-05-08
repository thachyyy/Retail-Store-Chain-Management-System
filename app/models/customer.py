from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID

class Customer(Base):
    __tablename__ = "customer"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    full_name = Column(String(255), unique = False, nullable = False)
    dob = Column(String(255), unique = False, nullable = True)
    gender = Column(String(8), unique = False, nullable = False)
    email = Column(String(255), unique = True, nullable = True)
    phone_number = Column(String(16), unique = True, nullable = False)
    address = Column(String(255), unique = False, nullable = True)
    district = Column(String(64), unique = False, nullable = True)
    province = Column(String(64), unique = False, nullable = True)
    reward_point = Column(String, unique = False, nullable = False)
    note = Column(String, unique = False, nullable = True)    
    tenant_id = Column(String, unique = False, nullable = False)