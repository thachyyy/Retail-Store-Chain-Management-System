import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class InventoryCheckDetail(BaseModel):
    branch_id: str
    product_id: str
    batch_id: str
    quantity: int

class InventoryCheckDetailResponse(BaseModel):
    branch_id: str
    product_id: str
    batch_id: str
    real_quantity: int
    quantiry_in_db: int
    difference: int
    
class InventoryCheckDetailCreate(BaseModel):
    branch_id: str
    product_id: str
    batch_id: str
    real_quantity: int
    quantity_in_db: int
    difference: int
    tenant_id: str
    branch: str