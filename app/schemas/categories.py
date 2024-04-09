from typing import Optional
from pydantic import BaseModel, validator

class CategoriesCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    
class CategoriesCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    
class CategoriesUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
    @validator('name', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value