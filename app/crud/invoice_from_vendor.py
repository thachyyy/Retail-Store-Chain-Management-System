import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.invoice_from_vendor import InvoiceFromVendorCreate, InvoiceFromVendorUpdate
from app.crud.base import CRUDBase
from ..models import InvoiceFromVendor

logger = logging.getLogger(__name__)


class CRUDInvoiceFromVendor(CRUDBase[InvoiceFromVendor, InvoiceFromVendorCreate, InvoiceFromVendorUpdate]):    
    @staticmethod
    async def get_all_invoice_from_vendors(db: Session) -> Optional[InvoiceFromVendor]:
        return db.query(InvoiceFromVendor).all()
    
    @staticmethod
    async def get_invoice_from_vendor_by_phone(db: Session, phone_number: str) -> Optional[InvoiceFromVendor]:
        return db.query(InvoiceFromVendor).filter(InvoiceFromVendor.phone_number == phone_number).first()
    
    @staticmethod
    async def get_invoice_from_vendor_by_email(db: Session, email: EmailStr) -> Optional[InvoiceFromVendor]:
        return db.query(InvoiceFromVendor).filter(InvoiceFromVendor.email == email).first()
    
    @staticmethod
    async def get_invoice_from_vendor_by_id(db: Session, invoice_from_vendor_id: str):
        return db.query(InvoiceFromVendor).filter(InvoiceFromVendor.id == invoice_from_vendor_id).first()
    
    @staticmethod
    async def update_invoice_from_vendor(db: Session, invoice_from_vendor_id: str, invoice_from_vendor_update: InvoiceFromVendorUpdate):
        update_data = invoice_from_vendor_update.dict(exclude_none=True)
        return db.query(InvoiceFromVendor).filter(InvoiceFromVendor.id == invoice_from_vendor_id).update(update_data)
    
    @staticmethod
    async def delete_invoice_from_vendor(db: Session, invoice_from_vendor_id: str):
        return db.query(InvoiceFromVendor).filter(InvoiceFromVendor.id == invoice_from_vendor_id).delete()
    
    @staticmethod
    async def search_invoice_from_vendor(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_invoice_from_vendor(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: InvoiceFromVendorCreate) -> InvoiceFromVendor:
        logger.info("CRUDInvoiceFromVendor: create called.")
        logger.debug("With: InvoiceFromVendorCreate - %s", obj_in.dict())

        db_obj = InvoiceFromVendor(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDInvoiceFromVendor: create called successfully.")
        return db_obj

invoice_from_vendor = CRUDInvoiceFromVendor(InvoiceFromVendor)
