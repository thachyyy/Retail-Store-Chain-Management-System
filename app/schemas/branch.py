from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
import enum
from .employee import EmployeeCreate
class Status(str,enum.Enum):
    ACTIVE= "Đang hoạt động"
    INACTIVE="Dừng hoạt động"
class BranchCreateParams(BaseModel):
    name_display:  str
    name_detail:  str
    address:  str
    status: Status
    district: Optional[str] = None
    province: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    note: Optional[str] = None
    
    
class BranchCreate(BaseModel):
    id: str
    name_display:  str
    name_detail:  str
    address:  str
    status: Status
    district: Optional[str] = None
    province: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    note: Optional[str] = None
    class Config:
        orm_mode = True
    
class BranchUpdate(BaseModel):
    name_display: Optional[str] = None
    name_detail: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    status: Optional[Status] = None
    note: Optional[str] = None

class BranchResponse(BranchCreate):
    employees: List[EmployeeCreate]
