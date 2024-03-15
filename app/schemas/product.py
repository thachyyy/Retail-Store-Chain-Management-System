from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field
import enum
class Status(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
    EMPTY= "EMPTY"
class ProductCreateParams(BaseModel):
    barcode: str = Field(..., max_length=255)
    product_name: str = Field(..., max_length=255)
    unit: str = Field(..., max_length=255)
    sale_price: int
    status: Status = Status.EMPTY
    last_purchase_price: Optional[int]
    description: Optional[str] = Field(None, max_length=255)
    categories: Optional[str] = Field(None, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    note: Optional[str] = Field(None, max_length=255)
    contract_for_vendor_id: Optional[UUID4] = None
    promotion_id: Optional[UUID4] = None
    batch_id: Optional[UUID4] = None
    has_promotion: Optional[bool] = Field(default=False)
    
class ProductCreate(BaseModel):
    barcode: str 
    product_name: str
    unit: str
    sale_price: int
    status: Status
    last_purchase_price: Optional[int] = None
    description: Optional[str] = None
    categories: Optional[str] = None 
    brand: Optional[str] = None 
    note: Optional[str] = None 
    contract_for_vendor_id: Optional[UUID4] = None
    promotion_id: Optional[UUID4] = None
    batch_id: Optional[UUID4] = None
    has_promotion: Optional[bool] = None 
    
class ProductUpdate(BaseModel):
    barcode: Optional[str] = Field(None, max_length=255)
    product_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    categories: Optional[str] = Field(None, max_length=255)
    brand: Optional[str] = Field(None, max_length=255)
    unit: Optional[str] = Field(None, max_length=255)
    last_purchase_price: Optional[int]
    sale_price: Optional[int]
    status: Optional[Status]
    note: Optional[str] = Field(None, max_length=255)
    contract_for_vendor_id: Optional[UUID4]
    promotion_id: Optional[UUID4]
    batch_id: Optional[UUID4]
    has_promotion: Optional[bool]



class ProductResponse(ProductCreate):
    class Config:
        orm_mode = True
        