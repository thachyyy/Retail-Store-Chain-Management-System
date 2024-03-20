from typing import Optional, Literal
from pydantic import BaseModel, UUID4
from datetime import datetime

class PromotionBelongToBranchCreateParams(BaseModel):
    prmotion_id: str
    branch_id: str
    
class PromotionBelongToBranchCreate(BaseModel):
    id: str
    promotion_id: str
    branch_id: str
    
class PromotionBelongToBranchUpdate(BaseModel):
    promotion_id: Optional[str]
    branch_id: Optional[str]