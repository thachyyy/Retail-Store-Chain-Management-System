import enum
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
class Status(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(String, primary_key=True)
    name = Column(String(255),nullable=False,unique=True)
    description = Column(String(255),nullable=True)
 