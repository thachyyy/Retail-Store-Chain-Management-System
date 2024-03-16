from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class OrderOfBatchCreateParams(BaseModel):
    price: int
    quantity: int
    purchase_order_id: UUID4
    batch_id: UUID4
    
class OrderOfBatchCreate(BaseModel):
    id: UUID4
    price: int
    quantity: int
    purchase_order_id: UUID4
    batch_id: UUID4

class OrderOfBatchUpdate(BaseModel):
    price: Optional[int]
    quantity: Optional[int]
    purchase_order_id: Optional[UUID4]
    batch_id: Optional[UUID4]