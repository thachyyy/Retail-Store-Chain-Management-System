from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class OrderOfBatchCreateParams(BaseModel):
    price: int
    quantity: int
    purchase_order_id: str
    batch_id: str
    
class OrderOfBatchCreate(BaseModel):
    id: str
    price: int
    quantity: int
    purchase_order_id: str
    batch_id: str

class OrderOfBatchUpdate(BaseModel):
    price: Optional[int]
    quantity: Optional[int]
    purchase_order_id: Optional[str]
    batch_id: Optional[str]