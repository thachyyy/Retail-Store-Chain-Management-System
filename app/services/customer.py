import logging
import uuid
from typing import Optional

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerCreateParams, CustomerUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_customer_by_id(self, customer_id: str):
        logger.info("CustomerService: get_customer_by_id called.")
        result = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_customers(
        self,
        limit: Optional[int] = None,
        offset:Optional[int] = None, 
        gender: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        province: Optional[str] = None,
        district: Optional[str] = None,
    ):
        
        
        conditions = dict()
        if gender:
            conditions['gender'] = gender
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            conditions['end_date'] = end_date
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
            
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(conditions)
            sql = f"SELECT * FROM public.customer {whereConditions};"
            count = f"SELECT COUNT(*)::INT FROM public.customer {whereConditions};"
            
            if offset is not None and limit is not None:
                sql = f"SELECT * FROM public.customer {whereConditions} LIMIT {limit} OFFSET {offset};"

            logger.info("CustomerService: filter_customer called.")
            result,total = await crud.customer.filter_customer(self.db, sql=sql, count=count)

            logger.info("CustomerService: filter_customer called successfully.")
        else: 
            logger.info("CustomerService: get_all_customers called.")
            result,total =  crud.customer.get_multi(db=self.db, skip=offset,limit=limit)
            logger.info("CustomerService: get_all_customers called successfully.")

        return dict(message_code=AppStatus.SUCCESS.message,total=total),result
    
    async def gen_id(self):
        newID: str
        lastID = await crud.customer.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'CUS' + newID
        
    async def create_customer(self, obj_in: CustomerCreateParams):
        logger.info("CustomerService: get_customer_by_phone called.")
        current_phone_number = await crud.customer.get_customer_by_phone(self.db, obj_in.phone_number)
        logger.info("CustomerService: get_customer_by_phone called successfully.")
        
        logger.info("CustomerService: get_customer_by_email called.")
        current_email = await crud.customer.get_customer_by_email(self.db, obj_in.email)
        logger.info("CustomerService: get_customer_by_email called successfully.")
        
        if current_phone_number:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        if current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCOUNT_ALREADY_EXIST)
        
        if obj_in.email:
            obj_in.email = obj_in.email.lower()
        
        newID = await self.gen_id()
        
        if obj_in.reward_point < 0: obj_in.reward_point = 0 # check constrain reward point
        
        customer_create = CustomerCreate(
            id=newID,
            full_name=obj_in.full_name,
            dob=obj_in.dob,
            gender=obj_in.gender,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            reward_point=obj_in.reward_point,
            note=obj_in.note,
        )
        
        logger.info("CustomerService: create called.")
        result = crud.customer.create(db=self.db, obj_in=customer_create)
        logger.info("CustomerService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message),customer_create
    
    async def update_customer(self, customer_id: str, obj_in: CustomerUpdate):
        logger.info("CustomerService: get_customer_by_id called.")
        isValidCustomer = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        if not isValidCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        if obj_in.reward_point is not None and obj_in.reward_point < 0: obj_in.reward_point = 0 # check constrain reward point
        
        logger.info("CustomerService: update_customer called.")
        result = await crud.customer.update_customer(db=self.db, customer_id=customer_id, customer_update=obj_in)
        logger.info("CustomerService: update_customer called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_customer(self, customer_id: str):
        logger.info("CustomerService: get_customer_by_id called.")
        isValidCustomer = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        if not isValidCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("CustomerService: delete_customer called.")
        result = await crud.customer.delete_customer(self.db, customer_id)
        logger.info("CustomerService: delete_customer called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
    async def whereConditionBuilderForSearch(self, condition: str) -> str:
        conditions = list()
        conditions.append(f"id::text ilike '%{condition}%'")
        conditions.append(f"full_name ilike '%{condition}%'")
        conditions.append(f"phone_number ilike '%{condition}%'")
        conditions.append(f"address ilike '%{condition}%'")
            
        whereCondition = "WHERE " + ' OR '.join(conditions)
        return whereCondition
    
    async def whereConditionBuilderForFilter(self, conditions: dict) -> str:
        whereList = list()
        
        if 'gender' in conditions:
            whereList.append(f"gender = '{conditions['gender']}'")
        if 'province' in conditions:
            whereList.append(f"province = '{conditions['province']}'")
        if 'district' in conditions:
            whereList.append(f"district = '{conditions['district']}'")
        if 'start_date' in conditions:
            whereList.append(f"dob >= '{conditions['start_date']}'")
        if 'end_date' in conditions:
            whereList.append(f"dob <= '{conditions['end_date']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def search_customer(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.customer {whereCondition};"
        
        logger.info("CustomerService: search_customer called.")
        result = await crud.customer.search_customer(self.db, sql)
        logger.info("CustomerService: search_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_customer(
        self,
        gender: str = None,
        start_date: date = None,
        end_date: date = None,
        province: str = None,
        district: str = None,
    ):
        conditions = dict()
        if gender:
            conditions['gender'] = gender
        if start_date:
            conditions['start_date'] = start_date
        if end_date:
            conditions['end_date'] = end_date
        if province:
            conditions['province'] = province
        if district:
            conditions['district'] = district
        
        whereConditions = await self.whereConditionBuilderForFilter(conditions)
        sql = f"SELECT * FROM public.customer {whereConditions};"
        
        logger.info("CustomerService: filter_customer called.")
        result = await crud.customer.filter_customer(self.db, sql)
        logger.info("CustomerService: filter_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        