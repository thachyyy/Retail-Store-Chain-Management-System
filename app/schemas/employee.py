from typing import Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr
from datetime import date

class EmployeeCreateParams(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
    email: EmailStr
    phone_number: str
    role: Literal['nhan vien', 'quan ly cua hang', 'quan ly']
    address: str
    district: str
    province: str
    status: Optional[Literal['ACTIVE', 'INACTIVE']] = None
    note: Optional[str] = None
    branch_name: str

class EmployeeCreate(BaseModel):
    id: UUID4
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
    email: EmailStr
    phone_number: str
    role: Literal['nhan vien', 'quan ly cua hang', 'quan ly']
    address: str
    district: str
    province: str
    status: Optional[Literal['ACTIVE', 'INACTIVE']] = None
    note: Optional[str] = None
    branch_name: str
    
class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    role: Optional[Literal['nhan vien', 'quan ly cua hang', 'quan ly']] = None
    branch_name: Optional[str]