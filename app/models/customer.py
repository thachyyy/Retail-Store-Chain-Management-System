from sqlalchemy import Boolean, Column, String
from .base import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String(255), primary_key=True)
    full_name = Column(String(255), unique=False, nullable=False)
    dob = Column(String(255), unique=False, nullable=True)
    gender = Column(String(8), unique=False, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(16), unique=True, nullable=False)
    address = Column(String(255), unique=False, nullable=True)
    district = Column(String(64), unique=False, nullable=True)
    province = Column(String(64), unique=False, nullable=True)
    reward_point = Column(String, unique=False, nullable=False)
    note = Column(String, unique=False, nullable=True)
    