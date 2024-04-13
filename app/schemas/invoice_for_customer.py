from datetime import date
from typing import List, Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum

class PaymentMethod(str,enum.Enum):
    Momo = "Momo"
    InternetBanking = "Internet Banking"
    Cash = "Tiền mặt"
    

class InvoiceForCustomerCreateParams(BaseModel):
    total: int
    # status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    # belong_to_order: str
    order_detail: List[int]
     
class InvoiceForCustomerCreate(BaseModel):
    id: str
    total: int
    status: str = Field(default="Đã thanh toán")
    payment_method: PaymentMethod = Field(default=PaymentMethod.Cash)
    # belong_to_order: str
    order_detail: List[int] 

    
class InvoiceForCustomerUpdate(BaseModel):
    total: Optional[int] = None
    status: Optional[str] = Field(default="Đã thanh toán")
    payment_method: Optional[PaymentMethod] = Field(default=PaymentMethod.Cash)
    # belong_to_order: Optional[str] = None

class InvoiceForCustomerResponse(InvoiceForCustomerCreate):
    class Config:
        orm_mode = True
        