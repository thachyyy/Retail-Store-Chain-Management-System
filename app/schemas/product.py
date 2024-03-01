from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field
import enum
class Status(str,enum.Enum):
    ACTIVE = "ACTIVE" #Đang kinh doanh
    INACTIVE = "INACTIVE" #Tạm ngừng kinh doanh
    PENDING = "PENDING" #Hết hàng
    EMPTY = "EMPTY" #Trống
class ProductCreateParams(BaseModel):
    barcode: Optional[str] = Field(None, max_length=255)
    product_name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    categories: Optional[str] = Field(None, max_length=255)
    brand: str = Field(..., max_length=255)
    unit: Optional[str] = Field(None, max_length=255)
    last_purchase_price: int
    sale_price: int
    status: Status = Status.EMPTY
    note: Optional[str] = Field(None, max_length=255)
    contract_id: Optional[UUID4] = None
    promotion_id: Optional[UUID4] = None
    batch_id: Optional[UUID4] = None
    has_promotion: bool = Field(default=False)
    
class ProductCreate(BaseModel):
    id: UUID4
    barcode: str 
    product_name: str
    description: Optional[str] = None
    categories: Optional[str] = None 
    brand: str 
    unit: Optional[str] = None 
    last_purchase_price: int
    sale_price: int
    status: Status
    note: Optional[str] = None 
    contract_id: Optional[UUID4] = None
    promotion_id: Optional[UUID4] = None
    batch_id: Optional[UUID4] = None
    has_promotion: bool 
    
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
    contract_id: Optional[UUID4]
    promotion_id: Optional[UUID4]
    batch_id: Optional[UUID4]
    has_promotion: Optional[bool]


class ProductResponse(ProductCreate):
    class Config:
        orm_mode = True
        