from sqlalchemy import Column, Integer,  Date, ForeignKey, String, DateTime
from sqlalchemy.sql import text
from .base import Base

class InventoryCheckDetail(Base):
    
    __tablename__ = "inventory_check_detail"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    tenant_id = Column(String)
    branch_id = Column(String)
    product_id = Column(String)
    batch_id = Column(String)
    real_quantity = Column(Integer)
    quantity_in_db = Column(Integer)
    difference = Column(Integer)
    branch = Column(String)