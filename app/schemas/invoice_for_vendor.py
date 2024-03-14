from datetime import date
from typing import Optional
from pydantic import BaseModel, UUID4, Field
from datetime import datetime
import enum


class InvoiceForVendorCreateParams(BaseModel):
    payment_deadline: date
    total: int
    status: str
    vendor_id: UUID4

class InvoiceForVendorCreate(BaseModel):
    id: UUID4
    payment_deadline: date
    total: int
    status: str
    vendor_id: UUID4
    
class InvoiceForVendorUpdate(BaseModel):
    payment_deadline: Optional[date] = None
    total: Optional[int] = None
    status: Optional[str] = None

class InvoiceForVendorResponse(InvoiceForVendorCreate):
    class Config:
        orm_mode = True
        