from typing import Optional
from pydantic import BaseModel

class ContractForProductCreateParams(BaseModel):
    contract_id: str
    product_id: str
    price: int
    
class ContractForProductCreate(BaseModel):
    id: str
    contract_id: str
    product_id: str
    price: int

class ContractForProductUpdate(BaseModel):
    pass