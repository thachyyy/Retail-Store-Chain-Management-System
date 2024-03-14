from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr

class BranchCreateParams(BaseModel):
    name_display: str
    name_detail: str
    address: str
    district: Optional[str] = None
    province: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[Literal['OPEN', 'SUSPEND', 'UNDER RENOVATION', 'CLOSED', 'COMMING SOON']] = None
    note: Optional[str] = None
    manager_name: Optional[str] = None
    manager_id: Optional[UUID4]= None
    
class BranchCreate(BaseModel):
    id: UUID4
    name_display: str
    name_detail: str
    address: str
    district: Optional[str] = None
    province: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[Literal['OPEN', 'SUSPEND', 'UNDER RENOVATION', 'CLOSED', 'COMMING SOON']] = None
    note: Optional[str] = None
    manager_name: Optional[str] = None
    manager_id: Optional[UUID4] = None
    
class BranchUpdate(BaseModel):
    name_display: Optional[str] = None
    name_detail: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    status: Optional[Literal['OPEN', 'SUSPEND', 'UNDER RENOVATION', 'CLOSED', 'COMMING SOON']] = None
    note: Optional[str] = None
    manager_name: Optional[str] = None
    manager_id: Optional[UUID4] = None