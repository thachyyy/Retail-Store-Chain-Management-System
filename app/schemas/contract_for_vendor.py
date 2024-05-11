from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date

class ContractForVendorCreateParams(BaseModel):
    start_date: date
    end_date: date
    belong_to_vendor: str
    minimum_order_amount: Optional[int]
    minimum_order_quantity: Optional[int]
    ordering_cycle_amount: Optional[int]
    ordering_cycle_quantity: Optional[int]
    period: Optional[int]
    
    
class ContractForVendorCreate(BaseModel):
    id: str
    start_date: date
    end_date: date
    minimum_order_amount: Optional[int]
    minimum_order_quantity: Optional[int]
    ordering_cycle_amount: Optional[int]
    ordering_cycle_quantity: Optional[int]
    belong_to_vendor: str
    tenant_id: str
    branch: str
    period: Optional[int]

class ContractForVendorUpdate(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    minimum_order_amount: Optional[int]
    minimum_order_quantity: Optional[int]
    ordering_cycle_amount: Optional[int]
    ordering_cycle_quantity: Optional[int]
    belong_to_vendor: Optional[str]
    # pdf_url :Optional[str]
    period: Optional[int]