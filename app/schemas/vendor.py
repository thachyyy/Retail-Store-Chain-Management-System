from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, validator
import enum
class Status(str, enum.Enum):
    ACTIVE = "Đang hợp tác"
    INACTIVE = "Dừng hợp tác"

class VendorCreateParams(BaseModel):
    company_name: str
    vendor_name: str
    phone_number: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    district : Optional[str]
    province: Optional[str]
    status: Optional[str]
    note: Optional[str]

class VendorCreate(BaseModel):
    id: str
    company_name: str
    vendor_name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district : Optional[str] = None
    province: Optional[str] = None
    status: Status
    note: Optional[str] = None
    tenant_id: str

class VendorUpdate(BaseModel):
    company_name: Optional[str]
    vendor_name: Optional[str]
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district : Optional[str] = None
    province: Optional[str] = None
    status: Optional[Status]
    note: Optional[str] = None
    
    @validator('company_name', 'vendor_name', 'status', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value