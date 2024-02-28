from datetime import datetime
import enum
from sqlalchemy import Column, Enum, Integer, String, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
class CategoriesStatus(str,enum.Enum):
    ACTIVE = "Đang kinh doanh" #Đang kinh doanh
    INACTIVE = "Tạm ngừng kinh doanh" #Tạm ngừng kinh doanh
    PENDING = "Hết hàng" #Hết hàng
    EMPTY = "Trống" #Trống
class categories(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255),nullable=False)
    description = Column(String(255),nullable=True)
    has_promotion = Column(Boolean, nullable=False,default="No")
    status = Column(String(255),nullable=False,default="EMPTY")