from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, constr, Field, EmailStr, UUID4

class CustomerCreateParams(BaseModel):
    fullName: str
    dob: Optional[str] = None
    gender: str
    email: Optional[EmailStr] = None
    phone: str
    address: str
    district: Optional[str]
    province: Optional[str]
    reward_point: Optional[int] = 0
    note: Optional[str] = None
    
class CustomerCreate(BaseModel):
    id: UUID4
    full_name: str
    dob: Optional[str] = None
    gender: str
    email: Optional[EmailStr] = None
    phone: str
    address: str
    district: Optional[str]
    province: Optional[str]
    reward_point: Optional[int] = 0
    note: Optional[str] = None