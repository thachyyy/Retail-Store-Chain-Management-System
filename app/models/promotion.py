import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DateTime
from sqlalchemy.sql import text
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
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    promotion_code = Column(String(20), nullable=False, unique=True)
    promotion_name = Column(String(255), nullable=False)
    discount_percent = Column(Integer)
    discount_value_max = Column(Integer)
    min_total_valid = Column(Integer)
    remaining_number = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    branch = Column(String)
    tenant_id = Column(String, unique=False, nullable=False)
    
    # promotion_type = Column(String(255), nullable=False)  
    # promotion_value = Column(Integer, nullable=False)  
    # max_discount_amount = Column(Integer, nullable=False)
    # start_date = Column(DateTime, nullable=False)
    # end_date = Column(DateTime,nullable=False)
    # status = Column(String(16), nullable=False,default='ACTIVE')  
    # min_product_value = Column(Integer, nullable=True) 
    # min_product_quantity = Column(Integer, nullable=True)
    # vendor_id = Column(String,ForeignKey('vendor.id'),nullable=False,unique=False)
    # tenant_id = Column(String, unique=False, nullable=False)
    
    # vendor = relationship('Vendor')