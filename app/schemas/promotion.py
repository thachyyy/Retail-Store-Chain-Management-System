from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import datetime

class PromotionCreateParams(BaseModel):
    promotion_code: str
    promotion_name: str
    promotion_type: str
    promotion_value: int
    max_discount_amount: int
    start_date: datetime
    end_date: datetime
    status: Optional[Literal['ACTIVE', 'INACTIVE', 'EXPIRED', 'PENDING', 'CANCALLED']] = None
    min_product_value: Optional[int] = None
    min_product_quantity: Optional[int] = None
    
class PromotionCreate(BaseModel):
    id: str
    promotion_code: str
    promotion_name: str
    promotion_type: str
    promotion_value: int
    max_discount_amount: int
    start_date: datetime
    end_date: datetime
    status: Optional[Literal['ACTIVE', 'INACTIVE', 'EXPIRED', 'PENDING', 'CANCALLED']] = None
    min_product_value: Optional[int] = None
    min_product_quantity: Optional[int] = None
    
class PromotionUpdate(BaseModel):
    max_discount_amount: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[Literal['ACTIVE', 'INACTIVE', 'EXPIRED', 'PENDING', 'CANCALLED']] = None
    min_product_value: Optional[int] = None
    min_product_quantity: Optional[int] = None