from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class VendorCreateParams(BaseModel):
    company_name: Optional[str] = None
    vendor_name: str
    phone_number: str
    email: EmailStr
    address: str
    district : Optional[str] = None
    province: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None

class VendorCreate(BaseModel):
    id: UUID4
    company_name: Optional[str] = None
    vendor_name: str
    phone_number: str
    email: EmailStr
    address: str
    district : Optional[str] = None
    province: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None

class VendorUpdate(BaseModel):
    company_name: Optional[str] = None
    address: str
    district : Optional[str] = None
    province: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None