from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class CustomerCreateParams(BaseModel):
    full_name: str
    dob: Optional[date] = None
    gender: str
    email: Optional[EmailStr] = None
    phone_number: str
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = 0
    note: Optional[str] = None
    
class CustomerCreate(BaseModel):
    id: str
    full_name: str
    dob: Optional[date] = None
    gender: str
    email: Optional[EmailStr] = None
    phone_number: str
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = 0
    note: Optional[str] = None
    
class CustomerUpdate(BaseModel):
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = None
    note: Optional[str] = None

class CustomerResponse(BaseModel):
    pass