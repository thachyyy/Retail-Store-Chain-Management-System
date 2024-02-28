from sqlalchemy import Column, String, ForeignKey
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Branch(Base):
    __tablename__ = "branch"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), unique = False, nullable = False)
    address = Column(String(255), unique = True, nullable = False)
    district = Column(String(255), unique = False, nullable = True)
    province = Column(String(255), unique = False, nullable = True)
    phone_number = Column(String(255), unique = True, nullable = True)
    email = Column(String(255), unique = True, nullable = True)
    status = Column(String(255), unique = False, nullable = True)
    note = Column(String(255), unique = False, nullable = True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey('employee.id'), unique = True, nullable = True)
    
    employee = relationship('Employee')