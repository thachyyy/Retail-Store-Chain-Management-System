from typing import List, Optional
from pydantic import BaseModel, Field,validator

class BranchEmployee(BaseModel):
    branch: Optional[str]
    employee: Optional[str]
class BranchEmployeeCreate(BaseModel):
    pass
class BranchEmployeeUpdate(BaseModel):
    pass