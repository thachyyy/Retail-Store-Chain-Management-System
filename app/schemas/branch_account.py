from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator

class BranchAccountCreateParams(BaseModel):
    full_name: str
    branch_name: str
    phone_number: str
    password: str
    password_comfirm: str

class BranchAccountCreate(BaseModel):
    full_name: str
    branch_name: str
    phone_number: str
    hash_password: str
    
class BranchAccountLogin(BaseModel):
    phone_number: str
    password: str

class BranchAccountUpdate(BaseModel):
    pass