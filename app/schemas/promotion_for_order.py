from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import datetime

class PromotionForOrderCreateParams(BaseModel):
    promotion_id: UUID4
    purchase_order_id: UUID4
    
class PromotionForOrderCreate(BaseModel):
    id: UUID4
    promotion_id: UUID4
    purchase_order_id: UUID4

class PromotionForOrderUpdate(BaseModel):
    promotion_id: Optional[UUID4] = None
    purchase_order_id: Optional[UUID4] = None