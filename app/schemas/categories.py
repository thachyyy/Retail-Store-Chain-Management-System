from typing import Optional
from pydantic import BaseModel

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