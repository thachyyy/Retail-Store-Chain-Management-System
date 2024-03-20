
import logging
import uuid

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.invoice_from_vendor import InvoiceFromVendorResponse, InvoiceFromVendorCreate, InvoiceFromVendorCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class InvoiceFromVendorService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_invoice_from_vendor_by_id(self, invoice_from_vendor_id: str):
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called.")
        result = await crud.invoice_from_vendor.get_invoice_from_vendor_by_id(db=self.db, invoice_from_vendor_id=invoice_from_vendor_id)
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_invoice_from_vendors(self):
        logger.info("InvoiceFromVendorService: get_all_invoice_from_vendors called.")
        result = await crud.invoice_from_vendor.get_all_invoice_from_vendors(db=self.db)
        logger.info("InvoiceFromVendorService: get_all_invoice_from_vendors called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.invoice_from_vendor.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'INVOICEVEN' + newID
        
    async def create_invoice_from_vendor(self, obj_in: InvoiceFromVendorCreateParams):
        newID = await self.gen_id()
              
        invoice_from_vendor_create = InvoiceFromVendorCreate(
            id=newID,
            created_at=datetime.now(),
            payment_deadline=obj_in.payment_deadline,
            total=obj_in.total,
            status=obj_in.status,
            vendor_id=obj_in.vendor_id
        )
        
        logger.info("InvoiceFromVendorService: create called.")
        result = crud.invoice_from_vendor.create(db=self.db, obj_in=invoice_from_vendor_create)
        logger.info("InvoiceFromVendorService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_invoice_from_vendor success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=invoice_from_vendor_create)
    
    async def update_invoice_from_vendor(self, invoice_from_vendor_id: str, obj_in):
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called.")
        isValidInvoiceFromVendor = await crud.invoice_from_vendor.get_invoice_from_vendor_by_id(db=self.db, invoice_from_vendor_id=invoice_from_vendor_id)
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called successfully.")
        
        if not isValidInvoiceFromVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVOICE_FOR_VENDOR_NOT_FOUND)
        
        logger.info("InvoiceFromVendorService: update_invoice_from_vendor called.")
        result = await crud.invoice_from_vendor.update_invoice_from_vendor(db=self.db, invoice_from_vendor_id=invoice_from_vendor_id, invoice_from_vendor_update=obj_in)
        logger.info("InvoiceFromVendorService: update_invoice_from_vendor called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_invoice_from_vendor(self, invoice_from_vendor_id: str):
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called.")
        isValidInvoiceFromVendor = await crud.invoice_from_vendor.get_invoice_from_vendor_by_id(db=self.db, invoice_from_vendor_id=invoice_from_vendor_id)
        logger.info("InvoiceFromVendorService: get_invoice_from_vendor_by_id called successfully.")
        
        if not isValidInvoiceFromVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVOICE_FOR_VENDOR_NOT_FOUND)
        
        logger.info("InvoiceFromVendorService: delete_invoice_from_vendor called.")
        result = await crud.invoice_from_vendor.delete_invoice_from_vendor(self.db, invoice_from_vendor_id)
        logger.info("InvoiceFromVendorService: delete_invoice_from_vendor called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
