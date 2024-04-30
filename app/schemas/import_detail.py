import enum
from typing import List, Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import date


class ImportDetailCreateParams(BaseModel):
    product_id: str
    product_name: str
    unit: str
    import_price: int 
    quantity: int
    # manufacturing_date: date
    expiry_date : Optional[date] = None
    sub_total:int
    tenant_id:str
    branch:str
    # manufacturing_date: date
class ImportDetailCreate(ImportDetailCreateParams):
    id: str
    
  
class ImportDetailUpdate(BaseModel):
    pass
    