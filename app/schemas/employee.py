from typing import Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date
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
        
class EmployeeCreateParams(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    password: str
    role: Role
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    status: Status
    note: Optional[str] = None
    branch_name: Optional[str] = None

class EmployeeCreate(BaseModel):
    id: str
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: str
    password: str
    role: Role
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    status: Status
    note: Optional[str] = None
    branch_name: Optional[str] = None
    
class EmployeeUpdate(BaseModel):
    full_name: Optional[str]
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr]
    phone_number: Optional[str]
    password: Optional[str]
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    role: Optional[Role]
    branch_name: Optional[str]
    
    @validator('full_name', 'email', 'phone_number', 'password', 'role', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value