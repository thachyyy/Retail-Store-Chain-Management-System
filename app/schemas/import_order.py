from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date

class ImportOrderCreateParams(BaseModel):
    is_contract: bool
    estimated_date: date
    delivery_status: str
    payment_status: str
    subtotal: int
    promotion: Optional[int]
    total: int
    created_by: UUID4
    belong_to_vendor: UUID4
    belong_to_contract: UUID4
    belong_to_invoice: Optional[UUID4]
    
class ImportOrderCreate(BaseModel):
    id: UUID4
    is_contract: bool
    estimated_date: date
    delivery_status: str
    payment_status: str
    subtotal: int
    promotion: Optional[int]
    total: int
    created_by: UUID4
    belong_to_vendor: UUID4
    belong_to_contract: UUID4
    belong_to_invoice: Optional[UUID4]
    
class ImportOrderUpdate(BaseModel):
    is_contract: Optional[bool]
    estimated_date: Optional[date]
    delivery_status: Optional[str]
    payment_status: Optional[str]
    subtotal: Optional[int]
    promotion: Optional[int]
    total: Optional[int]
    created_by: Optional[UUID4]
    belong_to_vendor: Optional[UUID4]
    belong_to_contract: Optional[UUID4]
    belong_to_invoice: Optional[UUID4]
    