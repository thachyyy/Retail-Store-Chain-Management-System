from typing import List,Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date
# from .branch import BranchCreate

import enum
class Role(str,enum.Enum):
    STAFF = "Nhân viên"
    MANAGER = "Quản lý"
    BRANCH_MANAGER = "Quản lý chi nhánh"
class Status(str,enum.Enum):
    ACTIVE = "Đang làm việc"
    INACTIVE = "Nghỉ việc"
class Gender(str,enum.Enum):
    MALE = "Nam"
    FEMALE = "Nữ"

class EmployeeRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    branch: str
    password: str
    password_confirm: str
    
class EmployeeLogin(BaseModel):
    email: EmailStr
    password: str

   
class EmployeeCreateParams(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    role: Role
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    branch: str
    status: Status
    password: str
    note: Optional[str] = None
  

class EmployeeCreate(BaseModel):
    id: str
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    role: Role
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    status: Status
    branch: Optional[str]
    hashed_password: str
    tenant_id: str
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
    password: Optional[str] = None
    branch: Optional[str] = None
    # role: Optional[Role]
    
    
    @validator('full_name', 'email', 'phone_number', 'password', 'branch', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value