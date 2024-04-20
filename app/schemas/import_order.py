import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class PaymentStatus(str,enum.Enum):
    PAID = "Đã thanh toán"
    WAITING = "Chưa thanh toán"
class ImportOrderCreateParams(BaseModel):
    payment_status: PaymentStatus
    subtotal: int
    total: int
    belong_to_vendor: str
    is_contract: Optional[bool]
    belong_to_contract: Optional[str]
    estimated_date: Optional[date]
    promotion: Optional[int]
    list_import : Optional[List[int]]
    branch:str
    
class ImportOrderCreate(BaseModel):
    id: str
    payment_status: PaymentStatus
    subtotal: int
    total: int
    status:str 
    created_by: str
    belong_to_vendor: str
    tenant_id :str
    branch:str
    is_contract: Optional[bool]
    belong_to_contract: Optional[str]
    estimated_date: Optional[date]
    promotion: Optional[int]
    list_import : List[int]
class ImportOrderUpdate(BaseModel):
    is_contract: Optional[bool]
    estimated_date: Optional[date]
    payment_status: Optional[PaymentStatus]
    subtotal: Optional[int]
    status:Optional[str]
    promotion: Optional[int]
    total: Optional[int]
    created_by: Optional[str]
    belong_to_vendor: Optional[str]
    belong_to_contract: Optional[str]
    
class InvoiceOrderResponse(ImportOrderCreate):
    created_at: datetime
    updated_at: Optional[datetime]
  
    