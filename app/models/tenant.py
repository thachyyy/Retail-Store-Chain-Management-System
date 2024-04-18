from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Tenant(Base):
    __tablename__ = "tenant"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    tenant_id = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)