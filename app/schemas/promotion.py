from typing import Optional, Literal
from pydantic import BaseModel, UUID4, validator
from datetime import datetime
import enum
class Status(str,enum.Enum):
    ACTIVE = "Đang hiệu lực"
    INACTIVE = "Hết hiệu lực"

class PromotionCreateParams(BaseModel):
    promotion_code: str
    promotion_name: str
    discount_percent: int
    discount_value_max: int
    min_total_valid: int
    remaining_number: int
    start_date: datetime
    end_date: datetime
    status: Status
    
class PromotionCreate(BaseModel):
    id: str
    promotion_code: str
    promotion_name: str
    discount_percent: int
    discount_value_max: int
    min_total_valid: int
    remaining_number: int
    start_date: datetime
    end_date: datetime
    status: Status
    branch: str
    tenant_id: str
    
class PromotionUpdate(BaseModel):
    remaining_number: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[Status] = None
    
    @validator('remaining_number', 'start_date', 'end_date', 'status', pre=True, always=False)
    def check_not_null(cls, value, field):
        if value is None:
            raise ValueError(f"{field.name} cannot be null")
        return value