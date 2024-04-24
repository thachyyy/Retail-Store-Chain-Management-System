from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

'''
    Định nghĩa cột status:
    0: sắp tới hết hạn, hết hạn
    1: đã xử lý xong, không cần thông báo nữa
'''

class Noti(Base):
    __tablename__ = "noti"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    product_id = Column(String, nullable=False)
    product_name = Column(String)
    batch_id = Column(String, nullable=False)
    quantity = Column(Integer)
    message = Column(String)
    status = Column(Integer)
    tenant_id = Column(String, nullable=False)
    branch = Column(String, nullable=False)