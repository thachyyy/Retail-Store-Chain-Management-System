from sqlalchemy import ARRAY, Column, String,ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(String, primary_key=True)
    name_display = Column(String(255), unique = False, nullable = False) # Tên hiện thị (vd: Circle K,...)
    name_detail = Column(String(255), unique = True, nullable = False) # Tên chi tiết (vd: Circle K Thành Thái - Q10,...)
    address = Column(String(255), unique = True, nullable = False)
    district = Column(String(255), unique = False, nullable = True)
    province = Column(String(255), unique = False, nullable = True)
    phone_number = Column(String(255), unique = True, nullable = True)
    email = Column(String(255), unique = True, nullable = True)
    status = Column(String(16), unique = False, nullable = False, default = "ACTIVE")
    note = Column(String(255), unique = False, nullable = True)
    manager_name = Column(String(255), unique = True, nullable = True)
    manager_id = Column(String, ForeignKey('employee.id'), unique = True, nullable = True)
    employee = relationship('Employee')