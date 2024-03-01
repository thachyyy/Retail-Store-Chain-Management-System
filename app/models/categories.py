import enum
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
class Status(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
    PENDING = "PENDING" #Hết hàng
    EMPTY = "EMPTY" #Trống
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255),nullable=False)
    description = Column(String(255),nullable=True)
    has_promotion = Column(Boolean, nullable=False,default="No")