from datetime import date
from typing import Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum
class Status(str,enum.Enum):
    PAID = "Đã thanh toán"
    WAITING = "Đang chờ xử lí"
    CANCELED = "Hủy đơn đặt hàng"
    REFUNDED = "Hoàn trả tiền"
    FAILED = "Đặt hàng thất bại"
class PurchaseOrderCreateParams(BaseModel):
    estimated_delivery_date: datetime
    tax: Optional[float] = None
    subtotal: float
    promote: Optional[float] = None
    total: float
    tax_percentage: float
    status: Status = Field(default= Status.WAITING)
    note: Optional[str] = None
    belong_to_customer : Optional[str] = Field(None)
    
class PurchaseOrderCreate(BaseModel):
    id: UUID4
    created_at: datetime
    estimated_delivery_date: datetime
    tax: Optional[float]
    subtotal: float
    promote: Optional[float]
    total: float
    tax_percentage: float
    status: Optional[Status] = Field(default= Status.WAITING)
    note: Optional[str]
    handle_by: UUID4
    belong_to_customer: Optional[str]= Field(None)
    
class PurchaseOrderUpdate(BaseModel):
    estimated_delivery_date: Optional[datetime] = None
    tax: Optional[float] = None
    subtotal: Optional[float] = None
    promote: Optional[float] = None
    total: Optional[float] = None
    tax_percentage: Optional[float] = None
    status: Optional[Status] = Field(default= Status.WAITING)
    note: Optional[str] = None
    handle_by: Optional[UUID4] = None
    belong_to_customer: Optional[str] = None

class PurchaseOrderResponse(PurchaseOrderCreate):
    class Config:
        orm_mode = True