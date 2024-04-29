from typing import List, Optional
from pydantic import BaseModel, Field,validator

class OrderDetails(BaseModel):
    quantity: int
    sub_total: int
    price:int
    batch: str
    product_id: str
    product_name: str
    
class OrderDetailCreate(BaseModel):
    pass
class OrderDetailUpdate(BaseModel):
    pass
