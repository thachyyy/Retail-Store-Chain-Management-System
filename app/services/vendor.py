import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4
from typing import Optional

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.vendor import VendorCreateParams, VendorCreate, VendorUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class VendorService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_vendors(
        self,
        limit: Optional[int] = None,
        offset:Optional[int] = None,
        province: str = None,
        district: str = None,
        status: str = None,
        id: str = None,
        vendor_name: str = None,
        company_name: str = None,
        email: str = None,
        phone_number: str = None,
        address: str = None,
        note: str = None,
    ):
        conditions = dict()
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        if status:
            conditions['status'] = status
        if id:
            conditions['id'] = id
        if vendor_name:
            conditions['vendor_name'] = vendor_name
        if company_name:
            conditions['company_name'] = company_name
        if email:
            conditions['email'] = email
        if phone_number:
            conditions['phone_number'] = phone_number
        if address:
            conditions['address'] = address
        if note:
            conditions['note'] = note
            
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(conditions)
            sql = f"SELECT * FROM public.vendor {whereConditions};"
                
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.vendor {whereConditions} LIMIT {limit} OFFSET {offset};"
            logger.info("VendorService: filter_vendor called.")
            result = await crud.vendor.filter_vendor(self.db, sql=sql)
            total = len(result)
            logger.info("VendorService: filter_vendor called successfully.")
            
        else:
            logger.info("VendorService: get_all_vendors called.")
            result,total = await crud.vendor.get_all_vendors(self.db, offset, limit)
            logger.info("VendorService: get_all_vendors called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message, total=total), result
    
    async def get_vendor_by_id(self, vendor_id: str):
        logger.info("VendorService: get_vendor_by_id called.")
        result = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
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
        if obj_in.phone_number is not None:
            logger.info("VendorService: get_vendor_by_phone called.")
            current_phone_number = await crud.vendor.get_vendor_by_phone(self.db, obj_in.phone_number)
            logger.info("VendorService: get_vendor_by_phone called successfully.")
            if current_phone_number:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        
        if obj_in.email is not None:
            logger.info("VendorService: get_vendor_by_email called.")
            current_email = await crud.vendor.get_vendor_by_email(self.db, obj_in.email)
            logger.info("VendorService: get_vendor_by_email called successfully.")
            if current_email:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        if obj_in.email:
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
        return dict(message_code=AppStatus.SUCCESS.message), vendor_create
    
    async def update_vendor(self, vendor_id: str, obj_in):
        logger.info("VendorService: get_vendor_by_id called.")
        isValidVendor = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        if not isValidVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        if obj_in.phone_number is not None:
            logger.info("VendorService: get_vendor_by_phone called.")
            current_phone_number = await crud.vendor.get_vendor_by_phone(self.db, obj_in.phone_number, vendor_id)
            logger.info("VendorService: get_vendor_by_phone called successfully.")
            if current_phone_number:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        
        if obj_in.email is not None:
            logger.info("VendorService: get_vendor_by_email called.")
            current_email = await crud.vendor.get_vendor_by_email(self.db, obj_in.email, vendor_id)
            logger.info("VendorService: get_vendor_by_email called successfully.")
            if current_email:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        logger.info("VendorService: update_vendor called.")
        result = await crud.vendor.update_vendor(db=self.db, vendor_id=vendor_id, vendor_update=obj_in)
        logger.info("VendorService: update_vendor called successfully.")
        self.db.commit()
        obj_update = await crud.vendor.get_vendor_by_id(self.db, vendor_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_vendor(self, vendor_id: str):
        logger.info("VendorService: get_vendor_by_id called.")
        isValidVendor = await crud.vendor.get_vendor_by_id(db=self.db, vendor_id=vendor_id)
        logger.info("VendorService: get_vendor_by_id called successfully.")
        
        if not isValidVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        obj_del = await crud.vendor.get_vendor_by_id(self.db, vendor_id)
        
        logger.info("VendorService: delete_vendor called.")
        result = await crud.vendor.delete_vendor(self.db, vendor_id)
        logger.info("VendorService: delete_vendor called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"vendor_name ilike '%{condition}%'")
        # conditions.append(f"phone_number ilike '%{condition}%'")
        # conditions.append(f"email ilike '%{condition}%'")
        # conditions.append(f"address ilike '%{condition}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        # filter using '='
        if 'province' in conditions:
            whereList.append(f"province = '{conditions['province']}'")
        if 'district' in conditions:
            whereList.append(f"district = '{conditions['district']}'")
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
            
        # filter using 'ilike'
        if 'id' in conditions:
            whereList.append(f"id ilike '%{conditions['id']}%'")
        if 'vendor_name' in conditions:
            whereList.append(f"vendor_name ilike '%{conditions['vendor_name']}%'")
        if 'company_name' in conditions:
            whereList.append(f"company_name ilike '%{conditions['company_name']}%'")
        if 'email' in conditions:
            whereList.append(f"email ilike '%{conditions['email']}%'")
        if 'phone_number' in conditions:
            whereList.append(f"phone_number ilike '%{conditions['phone_number']}%'")
        if 'address' in conditions:
            whereList.append(f"address ilike '%{conditions['address']}%'")
        if 'note' in conditions:
            whereList.append(f"note ilike '%{conditions['note']}%'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
        
    async def search_vendor(
        self, 
        condition: str = None,
        limit: Optional[int] = None,
        offset:Optional[int] = None
    ):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.vendor {whereCondition};"
        
        if limit is not None and offset is not None:
            sql = f"SELECT * FROM public.vendor {whereCondition} LIMIT {limit} OFFSET {offset};"
        
        logger.info("VendorService: search_vendor called.")
        result = await crud.vendor.search_vendor(self.db, sql)
        logger.info("VendorService: search_vendor called successfully.")
        total = len(result)
        
        return dict(message_code=AppStatus.SUCCESS.message, total=total), result