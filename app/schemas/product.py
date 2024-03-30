from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field
import enum
class Status(str,enum.Enum):
    ACTIVE = "Đang kinh doanh" #Đang kinh doanh
    INACTIVE = "Tạm ngừng kinh doanh" #Tạm ngừng kinh doanh
class ProductCreateParams(BaseModel):
    barcode: str = Field(..., max_length=255)
    product_name: str = Field(..., max_length=255)
    unit: str = Field(..., max_length=255)
    sale_price: int
    status: Status = Status.ACTIVE
    last_purchase_price: Optional[int]
    description: Optional[str] = Field(None, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    note: Optional[str] = Field(None, max_length=255)
    categories_id: Optional[str] = None
    contract_for_vendor_id: Optional[str] = None
    promotion_id: Optional[str] = None
    batch_id: Optional[str] = None
    has_promotion: Optional[bool] = Field(default=False)
    
class ProductCreate(BaseModel):
    id: str
    barcode: str 
    product_name: str
    unit: str
    sale_price: int
    status: Status
    last_purchase_price: Optional[int] = None
    description: Optional[str] = None
    brand: Optional[str] = None 
    note: Optional[str] = None 
    categories_id: Optional[str] = None
    contract_for_vendor_id: Optional[str] = None
    promotion_id: Optional[str] = None
    batch_id: Optional[str] = None
    has_promotion: Optional[bool] = None 
    
class ProductUpdate(BaseModel):
    barcode: Optional[str] 
    product_name: Optional[str] 
    description: Optional[str] 
    brand: Optional[str] 
    unit: Optional[str] 
    last_purchase_price: Optional[int]
    sale_price: Optional[int]
    status: Optional[Status]
    note: Optional[str] 
    categories_id: Optional[str] 
    contract_for_vendor_id: Optional[str]
    promotion_id: Optional[str]
    batch_id: Optional[str]
    has_promotion: Optional[bool]



class ProductResponse(ProductCreate):
    class Config:
        orm_mode = True
        