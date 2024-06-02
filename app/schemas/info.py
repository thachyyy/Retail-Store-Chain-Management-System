import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class InfoCreate(BaseModel):
    product_id: str
    product_name: str
    sale_price: int
    sold: int
    sale_rate: float
    inventory: int
    tenant_id:str
    branch:str
    
class InfoUpdate(BaseModel):
    product_id: Optional[str]
    product_name: Optional[str]
    sale_price: Optional[int]
    sold:Optional[int] 
    sale_rate: Optional[float]
    inventory: Optional[int]
    category: Optional[str]
    class Config:
        orm_mode = True
class InvoiceOrderResponse(InfoCreate):
    pass
    