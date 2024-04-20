from datetime import date
from typing import List, Optional
from pydantic import BaseModel, UUID4, Field, validator
from datetime import datetime
import enum

from app.schemas.order_detail import OrderDetails
class Status(str,enum.Enum):
    PAID = "Đã thanh toán"
    WAITING = "Đang chờ xử lí"
    CANCELED = "Hủy đơn đặt hàng"
    REFUNDED = "Hoàn trả tiền"
    FAILED = "Đặt hàng thất bại"
class PurchaseOrderCreateParams(BaseModel):
    estimated_delivery_date: Optional[datetime]
    subtotal: int
    total: int
    tax_percentage: int
    tax: Optional[int] = None
    note: Optional[str] = None
    promote: Optional[int] = None
    # status: Status = Field(default= Status.WAITING)
    belong_to_customer : Optional[str] = Field(None)
    order_detail: List[OrderDetails]
class PurchaseOrderCreate(BaseModel):
    id: str
    # created_at: datetime
    estimated_delivery_date:Optional[datetime]
    subtotal: int
    total: int
    tax_percentage: int
    handle_by: str
    tax: Optional[int]
    promote: Optional[int]
    status: Optional[Status] = Field(default= Status.WAITING)
    note: Optional[str]
    belong_to_customer: Optional[str]= Field(None)
    tenant_id: str
    branch: str
    
class PurchaseOrderUpdate(BaseModel):
    estimated_delivery_date: Optional[datetime] = None
    tax: Optional[int] = None
    subtotal: Optional[int] = None
    promote: Optional[int] = None
    total: Optional[int] = None
    tax_percentage: Optional[int] = None
    status: Optional[Status] = Field(default= Status.WAITING)
    note: Optional[str] = None
    handle_by: Optional[str] = None
    belong_to_customer: Optional[str] = None
    
    @validator('estimated_delivery_date', 'subtotal', 'total', 'tax_percentage', 'handle_by', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value

class PurchaseOrderResponse(PurchaseOrderCreate):
    class Config:
        orm_mode = True