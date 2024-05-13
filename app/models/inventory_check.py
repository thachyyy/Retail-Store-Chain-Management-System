from sqlalchemy import Column, Integer,  Date, ForeignKey, String, DateTime, ARRAY
from sqlalchemy.sql import text
from .base import Base

class InventoryCheck(Base):
    
    __tablename__ = "inventory_check"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    tenant_id = Column(String)
    branch = Column(String)
    list_detail_id = Column(ARRAY(Integer))