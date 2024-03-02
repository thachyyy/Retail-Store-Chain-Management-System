from datetime import date
from typing import Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum

class PaymentMethod(str,enum.Enum):
    Momo = "Momo"
    InternetBanking = "Internet Banking"
    Cash = "Tiền mặt"
    

class InvoiceForCustomerCreateParams(BaseModel):
    total: float
    status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    belong_to_order: UUID4

class InvoiceForCustomerCreate(BaseModel):
    id: UUID4
    created_at: datetime
    total: float
    status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    belong_to_order: UUID4
    
class InvoiceForCustomerUpdate(BaseModel):
    total: Optional[float] = None
    status: Optional[str] = Field(default="Đã thanh toán")
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.Cash)
    belong_to_order: Optional[UUID4] = None

class InvoiceForCustomerResponse(InvoiceForCustomerCreate):
    class Config:
        orm_mode = True
        