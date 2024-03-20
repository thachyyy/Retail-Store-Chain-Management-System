from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import datetime

class PromotionForOrderCreateParams(BaseModel):
    promotion_id: str
    purchase_order_id: str
    
class PromotionForOrderCreate(BaseModel):
    id: str
    promotion_id: str
    purchase_order_id: str

class PromotionForOrderUpdate(BaseModel):
    promotion_id: Optional[str] = None
    purchase_order_id: Optional[str] = None