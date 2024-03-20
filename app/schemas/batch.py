from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr
from datetime import date

class BatchCreateParams(BaseModel):
    quantity: int
    import_price: int
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: str
    belong_to_receipt: str
    
class BatchCreate(BaseModel):
    id: str
    import_price: int
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: str
    belong_to_receipt: str
    
class BatchUpdate(BaseModel):
    import_price: Optional[int]
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    belong_to_branch: Optional[str]
    belong_to_receipt: Optional[str]