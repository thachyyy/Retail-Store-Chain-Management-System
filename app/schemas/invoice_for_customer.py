from datetime import date
from typing import List, Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum
from app.schemas.order_detail import OrderDetails

class PaymentMethod(str,enum.Enum):
    Momo = "Momo"
    InternetBanking = "Internet Banking"
    Cash = "Tiền mặt"
    

class InvoiceForCustomerCreateParams(BaseModel):
    total: int
    status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    belong_to_order: str
    order_detail: List[int]
    tenant_id :str
     
class InvoiceForCustomerCreate(BaseModel):
    id: str
    total: int
    status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    belong_to_order: str
    order_detail: List[int]
    tenant_id :str
    branch: str

    
class InvoiceForCustomerUpdate(BaseModel):
    total: Optional[int] = None
    status: Optional[str] = Field(default="Đã thanh toán")
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.Cash)
    belong_to_order: Optional[str] = None

class InvoiceForCustomerResponse(InvoiceForCustomerCreate):
    # class Config:
    #     orm_mode = True
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
    total: int
    payment_method: str
    status: str
    belong_to_order:str
    order_detail: Optional[list[int]]