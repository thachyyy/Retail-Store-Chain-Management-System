from datetime import datetime
import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
class PromotionStatus(str,enum.Enum):
    ACTIVE = "Sẵn sàng" #Đang kinh doanh
    INACTIVE = "Tạm ngưng" #Tạm ngừng kinh doanh
    EMPTY = "Không có" #Trống
class Promotion(Base):
    __tablename__ = 'promotion'

    id = Column(UUID(as_uuid=True), primary_key=True)
    promotion_code = Column(String(20), nullable=False, unique=True)
    promotion_name = Column(String(255), nullable=False)
    promotion_type = Column(String(255), nullable=False)  
    promotion_value = Column(Integer, nullable=False)  
    max_discount_amount = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime,nullable=False)
    status = Column(Enum(PromotionStatus), nullable=False,default=PromotionStatus.EMPTY)  
    min_product_value = Column(Integer, nullable=True) 
    min_product_quantity = Column(Integer, nullable=True)  
    #vendor_id = Column(String(255),nullable=False,unique=False)
    vendor_id = Column(String(255),ForeignKey('vendor.id'),nullable=False,unique=False)
    
    vendor = relationship('Vendor')