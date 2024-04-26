from sqlalchemy import ARRAY, Column, String, Date, Boolean,  ForeignKey, Integer, DateTime
from sqlalchemy.sql import text
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ImportOrder(Base):
    __tablename__ = "import_order"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=text("timezone('Asia/Ho_Chi_Minh', now())"))
    updated_at = Column(DateTime, onupdate=text("timezone('Asia/Ho_Chi_Minh', now())"))
    is_contract = Column(Boolean, unique = False, nullable = True)
    payment_status = Column(String, unique = False, nullable = False,default=("Chưa thanh toán"))
    total = Column(Integer, unique = False, nullable = False)
    estimated_date = Column(Date, unique = False, nullable = True)
    status = Column(String,nullable = False, default=("Đã nhập hàng"))
    created_by = Column(String, ForeignKey('employee.id'), unique = False, nullable = False)
    belong_to_vendor = Column(String(30), ForeignKey('vendor.id'), unique = False, nullable = False)
    belong_to_contract = Column(String(30), ForeignKey('contract_for_vendor.id'), unique = False, nullable = True)
    expiry_date = Column(Date,nullable = True,unique = False)
    list_import = Column(ARRAY(Integer), unique = False, nullable = True)
    tenant_id = Column(String, unique=False, nullable=False)
    branch = Column(String)
    note = Column(String,nullable=True,unique=False)
    employee = relationship('Employee')
    vendor = relationship('Vendor')
    contract_for_vendor = relationship('ContractForVendor')
