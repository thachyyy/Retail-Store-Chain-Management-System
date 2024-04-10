import enum 
from sqlalchemy import Column, ForeignKey, String,Integer,Enum,Boolean,DateTime
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import UUID

class Product(Base):
    __tablename__ = "product"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    barcode = Column(String(255), unique=True, nullable= False)
    product_name = Column(String(255),nullable=False)
    description = Column(String(255),nullable=True)
    
    brand = Column(String(255),nullable=True,index = True)
    unit = Column(String(255),nullable=False)
    last_purchase_price = Column(Integer,nullable=True,index = True)
    sale_price = Column(Integer,nullable=False,index = True)
    status = Column(String(50),nullable=False)
    note = Column(String(255),nullable=True)
    has_promotion = Column(Boolean,nullable=True, default="No")
    # categories = Column(String(255),nullable=True)
    # contract_for_vendor_id = Column(String,unique=False,nullable=True,index = True)
    # promotion_id = Column(String,unique=False,nullable=True,index = True)
    # batch_id = Column(String,unique=False,nullable=True,index = True)
    
    categories_id = Column(String,ForeignKey('categories.id'),nullable=True,index = True)
    contract_for_vendor_id = Column(String,ForeignKey('contract_for_vendor.id'),unique=False,nullable=True,index = True)
    promotion_id = Column(String,ForeignKey('promotion.id'),unique=False,nullable=True,index = True)
    batch_id = Column(String,ForeignKey('batch.id'),unique=False,nullable=True,index = True)
    
    categories = relationship('Categories')
    promotion = relationship('Promotion')
    contract_for_vendor = relationship('ContractForVendor')
    batch = relationship('Batch')