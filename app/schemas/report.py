from typing import List,Optional, Literal
from pydantic import BaseModel, UUID4, EmailStr, validator
from datetime import date

class ReportCreate(BaseModel):
    pass
    
class ReportUpdate(BaseModel):
    pass


class InventoryItem(BaseModel):
    product_name: str
    sold: int
    sale_price:int
class CategorizedItem(BaseModel):
    product_name: str
    sale_price:int
    average_consumption: int
    category: str