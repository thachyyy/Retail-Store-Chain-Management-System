import enum 
from sqlalchemy import Column, ForeignKey, String,Integer,Enum,Boolean
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
class ProductStatus(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
    PENDING = "PENDING" #Hết hàng
    EMPTY = "EMPTY" #Trống
class Product(Base):
    __tablename__ = "product"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    barcode = Column(String(255), unique=True, nullable= True)
    product_name = Column(String(255),nullable=False)
    description = Column(String(255),nullable=True)
    categories = Column(String(255),nullable=True)
    brand = Column(String(255),nullable=False,index = True)
    unit = Column(String(255),nullable=True)
    last_purchase_price = Column(Integer,nullable=False,index = True)
    sale_price = Column(Integer,nullable=False,index = True)
    status = Column(Enum(ProductStatus),nullable=False,default=ProductStatus.EMPTY)
    note = Column(String(255),nullable=True)
    # contract_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    # batch_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    # promotion_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    
    contract_id = Column(UUID(as_uuid=True),ForeignKey('contract.id'),unique=False,nullable=True,index = True)
    promotion_id = Column(UUID(as_uuid=True),ForeignKey('promotion.id'),unique=False,nullable=True,index = True)
    batch_id = Column(UUID(as_uuid=True),ForeignKey('batch.id'),unique=False,nullable=True,index = True)
    has_promotion = Column(Boolean,nullable=False, default="No")
    
    promotion = relationship('Promotion')
    contract = relationship('Contract')
    batch = relationship('Batch')