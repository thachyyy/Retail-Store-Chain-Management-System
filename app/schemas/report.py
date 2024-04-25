from typing import List,Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date

class ReportCreate(BaseModel):
    pass
    
class ReportUpdate(BaseModel):
    pass