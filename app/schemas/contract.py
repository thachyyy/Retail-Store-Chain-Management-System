from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date

class ContractCreateParams(BaseModel):
    start_date: date
    end_date: date
    minimum_order_amount: int
    minimum_order_quantity: int
    ordering_cycle_amount: int
    ordering_cycle_quantity: int
    belong_to_vendor: str
    
class ContractCreate(BaseModel):
    id: UUID4
    start_date: date
    end_date: date
    minimum_order_amount: int
    minimum_order_quantity: int
    ordering_cycle_amount: int
    ordering_cycle_quantity: int
    belong_to_vendor: str

class ContractUpdate(BaseModel):
    pass