from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class ProductOfImportOrderCreateParams(BaseModel):
    import_price: int
    product_id: UUID4
    import_order_id: UUID4
    
class ProductOfImportOrderCreate(BaseModel):
    id: UUID4
    import_price: int
    product_id: UUID4
    import_order_id: UUID4
    
class ProductOfImportOrderUpdate(BaseModel):
    import_price: Optional[int]
    product_id: Optional[UUID4]
    import_order_id: Optional[UUID4]