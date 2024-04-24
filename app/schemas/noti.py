from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date

class NotiCreateParams(BaseModel):
    pass

class NotiCreate(BaseModel):
    product_id: str
    product_name: str
    batch_id: str
    quantity: int
    message: str
    status: int
    tenant_id: str
    branch: str
    
class NotiUpdate(BaseModel):
    message: Optional[str]
    quantity: Optional[int]
    status: Optional[int]
    
    @validator('message', 'quantity', 'status', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value