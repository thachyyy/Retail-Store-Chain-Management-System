from datetime import datetime
import enum
from sqlalchemy import Column, Enum, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
from .base import Base  # Assuming .base is the correct import path for your Base
# Enum for the receipt status
class Status(str,enum.Enum):
    WAITING_FOR_CONFIRMATION = "Chờ xác nhận"
    COMFIRMED = "Đã xác nhận"
    PARTIALLY_RECEIVED = "Đã nhận một phần"
    RECEIVED = "Đã nhận hàng"
    CANCELLED = "Đã hủy"
    COMPLETED = "Hoàn thành"


class ImportTransaction(Base):
    __tablename__ = 'import_transaction'

    id = Column(UUID(as_uuid=True), primary_key=True)
    supplier_code = Column(String(50), nullable=False)
    creation_time = Column(DateTime, nullable=False)
    status = Column(Enum(Status), nullable=False,default=Status.WAITING_FOR_CONFIRMATION)
    receipt_id = Column(String(255),ForeignKey=('receipt.id'),nullable=False,unique=False)  # This can be an Enum if you have defined statuses
    total_amount = Column(Integer, nullable=True)  # Assuming 'Tổng số tiền' is an integer
    vendor_id = Column(String(255),ForeignKey=('vendor.id'),nullable=False,unique=False)
    store_id = Column(String(255),ForeignKey=('store.id'),nullable=False,unique=False)
    employee_id =Column(String(255),ForeignKey=('employee.id'),nullable=False,unique=False)
    
    vendor = relationship('Vendor') 
    store = relationship('Store') 
    receipt = relationship('Receipt')
    employee = relationship('Employee')