
from sqlalchemy import ARRAY, Column, String,ForeignKey, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class BranchEmployee(Base):
    __tablename__ = 'branch_employees'
    branch_id = Column(ForeignKey('branch.id'), primary_key=True)
    employee_id = Column(ForeignKey('employee.id'), primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    role = Column(String(25), unique = False, nullable = False)
    branch = relationship("Branch", back_populates="employees")
    employee = relationship("Employee", back_populates="branchs")

    # proxies
    employee_name = association_proxy(target_collection='employee', attr='full_name')
    branch_name = association_proxy(target_collection='branch', attr='name_detail')
