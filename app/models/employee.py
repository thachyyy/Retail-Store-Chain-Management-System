from sqlalchemy import Column, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

'''
    "ACTIVE" # Đang làm việc
    "INACTIVE" # Nghỉ việc
'''

class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    full_name = Column(String(255), unique = False, nullable = False)
    date_of_birth = Column(Date, unique = False, nullable = True)
    gender = Column(String(16), unique = False, nullable = True)
    email = Column(String(255), unique = True, nullable = False)
    phone_number = Column(String(32), unique = True, nullable = False)
    password = Column(String(255), unique = False, nullable = False)
    role = Column(String(25), unique = False, nullable = False)
    address = Column(String(255), unique = False, nullable = True)
    district = Column(String(255), unique = False, nullable = True)
    province = Column(String(255), unique = False, nullable = True)
    status = Column(String(255), unique = False, nullable = False, default = 'Đang làm việc')
    note = Column(String, unique = False, nullable = True)
    branchs= relationship("BranchEmployee", back_populates="employee")
 
