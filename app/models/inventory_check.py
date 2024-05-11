from sqlalchemy import Column, Integer,  Date, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base

class InventoryCheck(Base):
    __tablename__ = "inventory_check"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    tenant_id = Column(String)
    branch_id = Column(String)
    product_id = Column(String)
    batch_id = Column(String)
    real_quantity = Column(Integer)
    quantiry_in_db = Column(Integer)
    difference = Column(Integer)