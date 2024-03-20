import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
# class Status(str,enum.Enum):
#     ACTIVE = "ACTIVE" #Đang kinh doanh
#     INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
#     PENDING = "PENDING" #Hết hàng
#     EMPTY = "EMPTY" #Trống

'''
    "ACTIVE" # Còn hoạt động
    "INACTIVE" # Hết hoạt động - Hết số lượng mã khuyến mãi
    "EXPIRED" # Hết hạn
    "PENDING" # Đang chờ xử lý
    "CANCALLED" # Đã hủy
'''

class Promotion(Base):
    __tablename__ = 'promotion'

    id = Column(String, primary_key=True)
    promotion_code = Column(String(20), nullable=False, unique=True)
    promotion_name = Column(String(255), nullable=False)
    promotion_type = Column(String(255), nullable=False)  
    promotion_value = Column(Integer, nullable=False)  
    max_discount_amount = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime,nullable=False)
    status = Column(String(16), nullable=False,default='ACTIVE')  
    min_product_value = Column(Integer, nullable=True) 
    min_product_quantity = Column(Integer, nullable=True)
    vendor_id = Column(UUID,ForeignKey('vendor.id'),nullable=False,unique=False)
    
    vendor = relationship('Vendor')