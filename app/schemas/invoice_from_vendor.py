from datetime import date
from typing import Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum


class InvoiceFromVendorCreateParams(BaseModel):
    payment_deadline: date
    total: int
    status: str
    vendor_id: UUID4

class InvoiceFromVendorCreate(BaseModel):
    id: UUID4
    created_at: datetime
    payment_deadline: date
    total: int
    status: str
    vendor_id: UUID4
    
class InvoiceFromVendorUpdate(BaseModel):
    payment_deadline: Optional[date] = None
    total: Optional[int] = None
    status: Optional[str] = None

class InvoiceFromVendorResponse(InvoiceFromVendorCreate):
    class Config:
        orm_mode = True
        