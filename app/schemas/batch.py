from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date

class BatchCreateParams(BaseModel):
    quantity: int
    import_price: int
    product_id:str 
    belong_to_receipt: Optional[str]
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]

    class Config:
        orm_mode = True
    
class BatchCreate(BaseModel):
    id: str
    quantity: int
    import_price: int
    branch: str
    product_id:str 
    belong_to_receipt: Optional[str]
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    status: int
    tenant_id: str
    
class BatchUpdate(BaseModel):
    import_price: Optional[int]
    quantity: Optional[int]
    manufacturing_date: Optional[date]
    expiry_date: Optional[date]
    branch: Optional[str]
    belong_to_receipt: Optional[str]
    product_id: Optional[str]
    
    
    @validator('quantity', 'import_price', 'branch', 'product_id', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value
