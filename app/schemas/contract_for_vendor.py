from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date

class ContractForVendorCreateParams(BaseModel):
    start_date: date
    end_date: date
    minimum_order_amount: int
    minimum_order_quantity: int
    ordering_cycle_amount: int
    ordering_cycle_quantity: int
    belong_to_vendor: str
    
class ContractForVendorCreate(BaseModel):
    id: str
    start_date: date
    end_date: date
    minimum_order_amount: int
    minimum_order_quantity: int
    ordering_cycle_amount: int
    ordering_cycle_quantity: int
    belong_to_vendor: str

class ContractForVendorUpdate(BaseModel):
    pass