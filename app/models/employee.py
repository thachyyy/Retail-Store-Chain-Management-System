from sqlalchemy import Column, String, Date, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

'''
    "ACTIVE" # Đang làm việc
    "INACTIVE" # Nghỉ việc
'''

class Employee(Base):
    __tablename__ = "employee"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String(255), unique = False, nullable = False)
    date_of_birth = Column(Date, unique = False, nullable = True)
    gender = Column(String(16), unique = False, nullable = True)
    email = Column(String(255), unique = True, nullable = False)
    phone_number = Column(String(32), unique = True, nullable = False)
    role = Column(String(16), unique = False, nullable = False)
    address = Column(String(255), unique = False, nullable = False)
    district = Column(String(255), unique = False, nullable = False)
    province = Column(String(255), unique = False, nullable = False)
    status = Column(String(255), unique = False, nullable = False, default = 'ACTIVE')
    note = Column(String, unique = False, nullable = True)
    branch_name = Column(String(255), ForeignKey('branch.name_detail'), unique = False, nullable = False)