from typing import List,Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date

class TenantCreate(BaseModel):
    tenant_id: str
    email: EmailStr
    full_name: str
    
class TenantUpdate(BaseModel):
    pass