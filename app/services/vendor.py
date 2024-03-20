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
    
    async def gen_id(self):
        newID: str
        lastID = await crud.vendor.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'VEN' + newID
    
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
        
        newID = await self.gen_id()
        
        vendor_create = VendorCreate(
            id=newID,
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
    
    async def update_vendor(self, vendor_id: str, obj_in):
        logger.info("VendorService: get_vendor_by_id called.")
        isValidVendor = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        if not isValidVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("VendorService: update_vendor called.")
        result = await crud.vendor.update_vendor(db=self.db, vendor_id=vendor_id, vendor_update=obj_in)
        logger.info("VendorService: update_vendor called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_vendor(self, vendor_id: str):
        logger.info("VendorService: get_vendor_by_id called.")
        isValidVendor = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        if not isValidVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("VendorService: delete_vendor called.")
        result = await crud.vendor.delete_vendor(self.db, vendor_id)
        logger.info("VendorService: delete_vendor called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"vendor_name ilike '%{condition}%'")
        conditions.append(f"phone_number ilike '%{condition}%'")
        conditions.append(f"email ilike '%{condition}%'")
        conditions.append(f"address ilike '%{condition}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def search_vendor(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.vendors {whereCondition};"
        
        logger.info("VendorService: search_vendor called.")
        result = await crud.vendor.search_vendor(self.db, sql)
        logger.info("VendorService: search_vendor called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)