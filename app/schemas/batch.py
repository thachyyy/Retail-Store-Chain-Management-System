from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr
from datetime import date

class BatchCreateParams(BaseModel):
    quantity: int
    import_price: int
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: UUID4
    belong_to_receipt: UUID4
    
class BatchCreate(BaseModel):
    id: UUID4
    import_price: int
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: UUID4
    belong_to_receipt: UUID4
    
class BatchUpdate(BaseModel):
    import_price: Optional[int]
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: Optional[UUID4]
    belong_to_receipt: Optional[UUID4]