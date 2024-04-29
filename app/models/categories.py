import enum
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
class Status(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    name = Column(String(255),nullable=False,unique = True)
    description = Column(String(255),nullable=True)
    tenant_id = Column(String, unique=False, nullable=False)
    branch = Column(String, nullable=False)