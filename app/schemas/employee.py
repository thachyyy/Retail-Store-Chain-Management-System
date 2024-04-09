from typing import List,Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date
# from .branch import BranchCreate

import enum
class Role(str,enum.Enum):
    STAFF = "Nhân viên"
    MANAGER = "Quản lí"
    BRANCH_MANAGER = "Quản lí chi nhánh"
class Status(str,enum.Enum):
    ACTIVE = "Đang làm việc"
    ONBOARDING = "Thử việc"
    PART_TIME = "Bán thời gian"
    FULL_TIME ="Toàn thời gian"
    SUSPENDED ="Tạm ngưng làm việc"
class Gender(str,enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
        
class EmployeeCreateParams(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    role: Role
    address: str
    district: str
    province: str
    status: Optional[Status] = None
    note: Optional[str] = None
  

class EmployeeCreate(BaseModel):
    id: str
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    role: Role
    address: str
    district: str
    province: str
    status: Optional[Status] = None
    note: Optional[str] = None
    class Config:
        orm_mode = True

# class EmployeeResponse(EmployeeCreate):
#     branch: List[BranchCreate]
class EmployeeUpdate(BaseModel):
    full_name: Optional[str]
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr]
    phone_number: Optional[str]
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    role: Optional[Role]
    
    
    @validator('full_name', 'email', 'phone_number', 'role', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value
