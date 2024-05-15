import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class InventoryCheck(BaseModel):
    # list_detail_id: list[int]
    pass
class InventoryCheckResponse(BaseModel):
    pass
    
class InventoryCheckCreate(BaseModel):
    tenant_id: str
    branch: str
    list_detail_id: list[int]
    
class InventoryCheckResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    tenant_id: str
    branch: str
    list_detail_id: list[int]