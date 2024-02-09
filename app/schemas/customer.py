from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, constr, Field, EmailStr, UUID4

class CustomerCreateParams(BaseModel):
    full_name: str
    dob: Optional[str] = None
    gender: str
    email: Optional[EmailStr] = None
    phone_number: str
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = 0
    note: Optional[str] = None
    
class CustomerCreate(BaseModel):
    id: UUID4
    full_name: str
    dob: Optional[str] = None
    gender: str
    email: Optional[EmailStr] = None
    phone_number: str
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = 0
    note: Optional[str] = None
    
class CustomerUpdate(BaseModel):
    pass

class CustomerResponse(BaseModel):
    pass