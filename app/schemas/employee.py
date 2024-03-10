from typing import Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr
from datetime import date
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
    MALE = "Nam"
    FEMAIL = "Nữ"
        
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
    branch_name: str

class EmployeeCreate(BaseModel):
    id: UUID4
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
    branch_name: str
    
class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    role: Optional[Role] = None
    branch_name: Optional[str] = None