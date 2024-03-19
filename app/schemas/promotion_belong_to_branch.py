from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import datetime

class PromotionBelongToBranchCreateParams(BaseModel):
    prmotion_id: UUID4
    branch_id: UUID4
    
class PromotionBelongToBranchCreate(BaseModel):
    id: UUID4
    promotion_id: UUID4
    branch_id: UUID4
    
class PromotionBelongToBranchUpdate(BaseModel):
    promotion_id: Optional[UUID4]
    branch_id: Optional[UUID4]