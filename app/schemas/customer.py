from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
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
    dob: Optional[date]
    gender: str
    email: Optional[EmailStr]
    phone_number: str
    address: Optional[str]
    district: Optional[str]
    province: Optional[str]
    reward_point: Optional[int] = 0
    note: Optional[str]
    
class CustomerUpdate(BaseModel):
    full_name: Optional[str]
    dob: Optional[date]
    gender: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    address: Optional[str]
    district: Optional[str]
    province: Optional[str]
    reward_point: Optional[int]
    note: Optional[str]

class CustomerResponse(BaseModel):
    pass