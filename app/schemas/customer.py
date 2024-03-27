from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field
import enum

class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class CustomerCreateParams(BaseModel):
    full_name: str
    dob: Optional[date]
    gender: Gender = Gender.MALE
    email: Optional[EmailStr]
    phone_number: str
    address: Optional[str]
    district: Optional[str]
    province: Optional[str]
    reward_point: Optional[int] = 0
    note: Optional[str]
    
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
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int] = None
    note: Optional[str] = None

class CustomerResponse(BaseModel):
    pass