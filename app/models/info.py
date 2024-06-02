from sqlalchemy import ARRAY, JSON, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

class Info(Base):
    __tablename__ = "info"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    product_id = Column(String, unique = False, nullable = False)
    product_name = Column(String, unique = False, nullable = False)
    sale_price = Column(Integer, unique = False, nullable = False)
    sold = Column(Integer, unique = False, nullable = False)
    sale_rate = Column(Float, unique = False, nullable = False)
    inventory = Column(Integer, unique = False, nullable = False)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    branch = Column(String)
    tenant_id = Column(String, unique=False, nullable=False)
