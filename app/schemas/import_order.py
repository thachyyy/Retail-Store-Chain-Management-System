import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date

class PaymentStatus(str,enum.Enum):
    PAID = "Đã thanh toán"
    WAITING = "Chưa thanh toán"
class ImportOrderCreateParams(BaseModel):
    is_contract: bool
    delivery_status: str
    payment_status: PaymentStatus
    subtotal: int
    total: int
    belong_to_vendor: str
    belong_to_contract: Optional[str]
    estimated_date: Optional[date]
    promotion: Optional[int]
    # import_details : Optional[List[int]]
    
class ImportOrderCreate(BaseModel):
    id: str
    is_contract: bool
    delivery_status: str
    payment_status: PaymentStatus
    subtotal: int
    total: int
    status:str 
    created_by: str
    belong_to_vendor: str
    belong_to_contract: Optional[str]
    estimated_date: Optional[date]
    promotion: Optional[int]
    tenant_id :str
    # import_details : List[int]
    
class ImportOrderUpdate(BaseModel):
    is_contract: Optional[bool]
    estimated_date: Optional[date]
    delivery_status: Optional[str]
    payment_status: Optional[PaymentStatus]
    subtotal: Optional[int]
    status:Optional[str]
    promotion: Optional[int]
    total: Optional[int]
    created_by: Optional[str]
    belong_to_vendor: Optional[str]
    belong_to_contract: Optional[str]
    
    