import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.vendor import VendorCreateParams, VendorCreate, VendorUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class VendorService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_vendors(self):
        logger.info("VendorService: get_all_vendors called.")
        result = await crud.vendor.get_all_vendors(db=self.db)
        logger.info("VendorService: get_all_vendors called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_vendor_by_id(self, vendor_id: str):
        logger.info("VendorService: get_vendor_by_id called.")
        result = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_vendor(self, obj_in: VendorCreateParams):
        logger.info("VendorService: get_vendor_by_phone called.")
        current_phone_number = await crud.vendor.get_vendor_by_phone(self.db, obj_in.phone_number)
        logger.info("VendorService: get_vendor_by_phone called successfully.")
        
        logger.info("VendorService: get_vendor_by_email called.")
        current_email = await crud.vendor.get_vendor_by_email(self.db, obj_in.email)
        logger.info("VendorService: get_vendor_by_email called successfully.")
        
        if current_phone_number:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        if current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        obj_in.email = obj_in.email.lower()
        
        vendor_create = VendorCreate(
            id=uuid.uuid4(),
            company_name=obj_in.company_name,
            vendor_name=obj_in.vendor_name,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            status=obj_in.status,
            note=obj_in.note,
        )
        
        logger.info("VendorService: create called.")
        result = crud.vendor.create(db=self.db, obj_in=vendor_create)
        logger.info("VendorService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_vendor success.")
        return dict(message_code=AppStatus.SUCCESS.message)