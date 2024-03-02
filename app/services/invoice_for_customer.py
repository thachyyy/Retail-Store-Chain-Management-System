
import logging
import uuid

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.invoice_for_customer import InvoiceForCustomerResponse, InvoiceForCustomerCreate, InvoiceForCustomerCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from datetime import datetime
logger = logging.getLogger(__name__)

class InvoiceForCustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_invoice_for_customer_by_id(self, invoice_for_customer_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        result = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_invoice_for_customers(self):
        logger.info("InvoiceForCustomerService: get_all_invoice_for_customers called.")
        result = await crud.invoice_for_customer.get_all_invoice_for_customers(db=self.db)
        logger.info("InvoiceForCustomerService: get_all_invoice_for_customers called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        
    async def create_invoice_for_customer(self, obj_in: InvoiceForCustomerCreateParams):
     
              
        invoice_for_customer_create = InvoiceForCustomerCreate(
            id=uuid.uuid4(),
            created_at=datetime.now(),
            total=obj_in.total,
            status=obj_in.status,
            payment_method=obj_in.payment_method,
            belong_to_order=obj_in.belong_to_order,
        )
        
        logger.info("InvoiceForCustomerService: create called.")
        result = crud.invoice_for_customer.create(db=self.db, obj_in=invoice_for_customer_create)
        logger.info("InvoiceForCustomerService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_invoice_for_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_invoice_for_customer(self, invoice_for_customer_id: str, obj_in):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        if not isValidInvoiceForCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("InvoiceForCustomerService: update_invoice_for_customer called.")
        result = await crud.invoice_for_customer.update_invoice_for_customer(db=self.db, invoice_for_customer_id=invoice_for_customer_id, invoice_for_customer_update=obj_in)
        logger.info("InvoiceForCustomerService: update_invoice_for_customer called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_invoice_for_customer(self, invoice_for_customer_id: str):
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called.")
        isValidInvoiceForCustomer = await crud.invoice_for_customer.get_invoice_for_customer_by_id(db=self.db, invoice_for_customer_id=invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: get_invoice_for_customer_by_id called successfully.")
        
        if not isValidInvoiceForCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called.")
        result = await crud.invoice_for_customer.delete_invoice_for_customer(self.db, invoice_for_customer_id)
        logger.info("InvoiceForCustomerService: delete_invoice_for_customer called successfully.")
        
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
        if 'start_date' in conditions and 'end_date' in conditions:
            whereList.append(f"dob between '{conditions['start_date']}' and '{conditions['end_date']}'")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def search_invoice_for_customer(self, condition: str = None):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.invoice_for_customer {whereCondition};"
        
        logger.info("InvoiceForCustomerService: search_invoice_for_customer called.")
        result = await crud.invoice_for_customer.search_invoice_for_customer(self.db, sql)
        logger.info("InvoiceForCustomerService: search_invoice_for_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def filter_invoice_for_customer(
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
        sql = f"SELECT * FROM public.invoice_for_customer {whereConditions};"
        
        logger.info("InvoiceForCustomerService: filter_invoice_for_customer called.")
        result = await crud.invoice_for_customer.filter_invoice_for_customer(self.db, sql)
        logger.info("InvoiceForCustomerService: filter_invoice_for_customer called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        