import enum 
from sqlalchemy import Column, ForeignKey, String,Integer,Enum,Boolean
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import UUID

class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    barcode = Column(String(255), unique=True, nullable= False)
    product_name = Column(String(255),nullable=True)
    description = Column(String(255),nullable=True)
    categories = Column(String(255),nullable=True)
    brand = Column(String(255),nullable=True,index = True)
    unit = Column(String(255),nullable=False)
    last_purchase_price = Column(Integer,nullable=True,index = True)
    sale_price = Column(Integer,nullable=False,index = True)
    status = Column(String(50),nullable=False)
    note = Column(String(255),nullable=True)
    has_promotion = Column(Boolean,nullable=True, default="No")
    
    # contract_for_vendor_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    # promotion_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    # batch_id = Column(UUID(as_uuid=True),unique=False,nullable=True,index = True)
    
    contract_for_vendor_id = Column(UUID(as_uuid=True),ForeignKey('contract_for_vendor.id'),unique=False,nullable=True,index = True)
    promotion_id = Column(UUID(as_uuid=True),ForeignKey('promotion.id'),unique=False,nullable=True,index = True)
    batch_id = Column(UUID(as_uuid=True),ForeignKey('batch.id'),unique=False,nullable=True,index = True)
    
    promotion = relationship('Promotion')
    contract_for_vendor = relationship('ContractForVendor')
    batch = relationship('Batch')