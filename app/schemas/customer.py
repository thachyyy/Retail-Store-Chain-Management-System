from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4, Field, validator
import enum

class Gender(str, enum.Enum):
    MALE = "Nam"
    FEMALE = "Nữ"

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
    full_name: Optional[str]
    dob: Optional[date] = None
    gender: Optional[str]
    email: Optional[EmailStr] = None
    phone_number: Optional[str]
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    reward_point: Optional[int]
    note: Optional[str] = None
    
    @validator('full_name', 'gender', 'phone_number', 'reward_point', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value

class CustomerResponse(BaseModel):
    pass