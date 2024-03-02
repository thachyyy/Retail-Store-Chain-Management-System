from typing import Optional
from pydantic import BaseModel, UUID4

class CategoriesCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    
class CategoriesCreate(BaseModel):
    id: UUID4
    name: str
    description: Optional[str] = None
    
class CategoriesUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None