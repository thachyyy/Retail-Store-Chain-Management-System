from typing import Optional
from pydantic import BaseModel, UUID4

class ContractForProductCreateParams(BaseModel):
    contract_id: UUID4
    product_id: UUID4
    price: int
    
class ContractForProductCreate(BaseModel):
    id: UUID4
    contract_id: UUID4
    product_id: UUID4
    price: int

class ContractForProductUpdate(BaseModel):
    pass