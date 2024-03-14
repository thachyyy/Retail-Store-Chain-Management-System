import logging

from typing import Optional
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.invoice_for_vendor import InvoiceForVendorCreate, InvoiceForVendorUpdate
from app.crud.base import CRUDBase
from ..models import InvoiceForVendor

logger = logging.getLogger(__name__)


class CRUDInvoiceForVendor(CRUDBase[InvoiceForVendor, InvoiceForVendorCreate, InvoiceForVendorUpdate]):    
    @staticmethod
    async def get_all_invoice_for_vendors(db: Session) -> Optional[InvoiceForVendor]:
        return db.query(InvoiceForVendor).all()
    
    @staticmethod
    async def get_invoice_for_vendor_by_phone(db: Session, phone_number: str) -> Optional[InvoiceForVendor]:
        return db.query(InvoiceForVendor).filter(InvoiceForVendor.phone_number == phone_number).first()
    
    @staticmethod
    async def get_invoice_for_vendor_by_email(db: Session, email: EmailStr) -> Optional[InvoiceForVendor]:
        return db.query(InvoiceForVendor).filter(InvoiceForVendor.email == email).first()
    
    @staticmethod
    async def get_invoice_for_vendor_by_id(db: Session, invoice_for_vendor_id: str):
        return db.query(InvoiceForVendor).filter(InvoiceForVendor.id == invoice_for_vendor_id).first()
    
    @staticmethod
    async def update_invoice_for_vendor(db: Session, invoice_for_vendor_id: str, invoice_for_vendor_update: InvoiceForVendorUpdate):
        update_data = invoice_for_vendor_update.dict(exclude_none=True)
        return db.query(InvoiceForVendor).filter(InvoiceForVendor.id == invoice_for_vendor_id).update(update_data)
    
    @staticmethod
    async def delete_invoice_for_vendor(db: Session, invoice_for_vendor_id: str):
        return db.query(InvoiceForVendor).filter(InvoiceForVendor.id == invoice_for_vendor_id).delete()
    
    @staticmethod
    async def search_invoice_for_vendor(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_invoice_for_vendor(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    def create(db: Session, *, obj_in: InvoiceForVendorCreate) -> InvoiceForVendor:
        logger.info("CRUDInvoiceForVendor: create called.")
        logger.debug("With: InvoiceForVendorCreate - %s", obj_in.dict())

        db_obj = InvoiceForVendor(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDInvoiceForVendor: create called successfully.")
        return db_obj

invoice_for_vendor = CRUDInvoiceForVendor(InvoiceForVendor)
