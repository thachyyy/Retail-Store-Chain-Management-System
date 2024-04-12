from sqlalchemy import ARRAY, Column, Integer, String,ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

class BranchEmployee(Base):
    __tablename__ = 'branch_employees'
    id = Column(Integer, primary_key= True,autoincrement= True)
    branch_id = Column(ForeignKey('branch.id'))
    employee_id = Column(ForeignKey('employee.id'))
    branch = relationship("Branch", back_populates="employee")
    employee = relationship("Employee", back_populates="branch")

    # proxies
    # employee_name = association_proxy(target_collection='employee', attr='full_name')
    # branch_name = association_proxy(target_collection='branch', attr='name_detail')
