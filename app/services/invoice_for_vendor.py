
import logging
import uuid

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.invoice_for_vendor import InvoiceForVendorResponse, InvoiceForVendorCreate, InvoiceForVendorCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class InvoiceForVendorService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_invoice_for_vendor_by_id(self, invoice_for_vendor_id: str):
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called.")
        result = await crud.invoice_for_vendor.get_invoice_for_vendor_by_id(db=self.db, invoice_for_vendor_id=invoice_for_vendor_id)
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_invoice_for_vendors(self):
        logger.info("InvoiceForVendorService: get_all_invoice_for_vendors called.")
        result = await crud.invoice_for_vendor.get_all_invoice_for_vendors(db=self.db)
        logger.info("InvoiceForVendorService: get_all_invoice_for_vendors called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        
    async def create_invoice_for_vendor(self, obj_in: InvoiceForVendorCreateParams):
     
              
        invoice_for_vendor_create = InvoiceForVendorCreate(
            id=uuid.uuid4(),
            created_at=datetime.now(),
            payment_deadline=obj_in.payment_deadline,
            total=obj_in.total,
            status=obj_in.status,
            belong_to_order=obj_in.belong_to_order,
        )
        
        logger.info("InvoiceForVendorService: create called.")
        result = crud.invoice_for_vendor.create(db=self.db, obj_in=invoice_for_vendor_create)
        logger.info("InvoiceForVendorService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_invoice_for_vendor success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_invoice_for_vendor(self, invoice_for_vendor_id: str, obj_in):
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called.")
        isValidInvoiceForVendor = await crud.invoice_for_vendor.get_invoice_for_vendor_by_id(db=self.db, invoice_for_vendor_id=invoice_for_vendor_id)
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called successfully.")
        
        if not isValidInvoiceForVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVOICE_FOR_VENDOR_NOT_FOUND)
        
        logger.info("InvoiceForVendorService: update_invoice_for_vendor called.")
        result = await crud.invoice_for_vendor.update_invoice_for_vendor(db=self.db, invoice_for_vendor_id=invoice_for_vendor_id, invoice_for_vendor_update=obj_in)
        logger.info("InvoiceForVendorService: update_invoice_for_vendor called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_invoice_for_vendor(self, invoice_for_vendor_id: str):
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called.")
        isValidInvoiceForVendor = await crud.invoice_for_vendor.get_invoice_for_vendor_by_id(db=self.db, invoice_for_vendor_id=invoice_for_vendor_id)
        logger.info("InvoiceForVendorService: get_invoice_for_vendor_by_id called successfully.")
        
        if not isValidInvoiceForVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVOICE_FOR_VENDOR_NOT_FOUND)
        
        logger.info("InvoiceForVendorService: delete_invoice_for_vendor called.")
        result = await crud.invoice_for_vendor.delete_invoice_for_vendor(self.db, invoice_for_vendor_id)
        logger.info("InvoiceForVendorService: delete_invoice_for_vendor called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
