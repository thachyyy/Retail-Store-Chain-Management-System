from sqlalchemy import Boolean, Column, String, Integer
from .base import Base

class BranchAccount(Base):
    __tablename__ = "branch_account"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    branch_name = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    