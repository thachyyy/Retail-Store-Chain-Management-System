from sqlalchemy import ARRAY, Column, String,ForeignKey, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    name_display = Column(String(255), unique = False, nullable = False) # Tên hiện thị (vd: Circle K,...)
    name_detail = Column(String(255), unique = True, nullable = False) # Tên chi tiết (vd: Circle K Thành Thái - Q10,...)
    address = Column(String(255), unique = True, nullable = False)
    district = Column(String(255), unique = False, nullable = True)
    province = Column(String(255), unique = False, nullable = True)
    phone_number = Column(String(255), unique = True, nullable = True)
    email = Column(String(255), unique = True, nullable = True)
    status = Column(String(16), unique = False, nullable = False, default = "ACTIVE")
    note = Column(String(255), unique = False, nullable = True)
    employees = relationship('BranchEmployee', back_populates="branch")
