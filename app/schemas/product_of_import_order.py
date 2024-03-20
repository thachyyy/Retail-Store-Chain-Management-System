from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

class ProductOfImportOrderCreateParams(BaseModel):
    import_price: int
    product_id: str
    import_order_id: str
    
class ProductOfImportOrderCreate(BaseModel):
    id: str
    import_price: int
    product_id: str
    import_order_id: str
    
class ProductOfImportOrderUpdate(BaseModel):
    import_price: Optional[int]
    product_id: Optional[str]
    import_order_id: Optional[str]