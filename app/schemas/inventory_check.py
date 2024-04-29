import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date, datetime

class InventoryCheck(BaseModel):
    branch_id: str
    product_id: str
    batch_id: str
    quantity: int

class InventoryCheckResponse(BaseModel):
    branch_id: str
    product_id: str
    batch_id: str
    real_quantity: int
    quantiry_in_db: int
    difference: int